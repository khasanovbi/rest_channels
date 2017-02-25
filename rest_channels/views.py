# coding=utf-8
from __future__ import unicode_literals

from functools import update_wrapper

import six
from django.db import models
from rest_framework import exceptions, status
from rest_framework.compat import set_rollback

from rest_channels import exceptions as rest_exceptions
from rest_channels.settings import rest_channels_settings
from rest_channels.socket_request import ContentType, SocketRequest


def exception_handler(exc, context):
    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, dict):
            data = exc.detail
        else:
            data = {'detail': exc.detail}
        set_rollback()
        return data
    # Note: Unhandled exceptions will raise a 500 error.
    return None


class BaseChannelsView(object):
    # The following policies may be set at either globally, or per-view.
    text_renderer_class = rest_channels_settings.DEFAULT_TEXT_RENDERER_CLASS
    bytes_renderer_class = rest_channels_settings.DEFAULT_BYTES_RENDERER_CLASS

    text_parser_class = rest_channels_settings.DEFAULT_TEXT_PARSER_CLASS
    bytes_parser_class = rest_channels_settings.DEFAULT_BYTES_PARSER_CLASS

    settings = rest_channels_settings

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    @classmethod
    def as_view(cls, **initkwargs):
        if isinstance(getattr(cls, 'queryset', None), models.query.QuerySet):
            def force_evaluation():
                raise RuntimeError(
                    'Do not evaluate the `.queryset` attribute directly, '
                    'as the result will be cached and reused between requests. '
                    'Use `.all()` or call `.get_queryset()` instead.'
                )

            cls.queryset._fetch_all = force_evaluation
            cls.queryset._result_iter = force_evaluation  # Django <= 1.5

        for key in initkwargs:
            if key in cls.socket_channel_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(message, *args, **kwargs):
            self = cls(**initkwargs)
            self.message = message
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(message, *args, **kwargs)

        view.view_class = cls
        view.view_initkwargs = initkwargs

        update_wrapper(view, cls, updated=())
        update_wrapper(view, cls.dispatch, assigned=())
        view.cls = cls
        return view

    def _allowed_channels(self):
        return [channel_name for channel_name in self.socket_channel_names
                if hasattr(self, channel_name)]

    @property
    def allowed_channels(self):
        return self._allowed_channels()

    def not_allowed(self, request, *args, **kwargs):
        """
        If `message.method` does not correspond to a handler method,
        determine what kind of exception to raise.
        """
        raise rest_exceptions.EventNotAllowed(request.channel.name)

    def get_exception_handler_context(self):
        """
        Returns a dict that is passed through to EXCEPTION_HANDLER,
        as the `context` argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None)
        }

    def get_view_description(self, html=False):
        """
        Return some descriptive text for the view, as used in OPTIONS responses
        and in the browsable API.
        """
        func = self.settings.VIEW_DESCRIPTION_FUNCTION
        return func(self.__class__, html)

    def initialize_request(self, message, *args, **kwargs):
        """
        Returns the initial request object.
        """
        return SocketRequest(
            message,
            text_parser_class=self.text_parser_class,
            bytes_parser_class=self.bytes_parser_class
        )

    def get_renderer(self):
        if self.request.content_type == ContentType.text:
            return self.text_renderer_class
        else:
            return self.bytes_renderer_class

    def get_rendered_data(self, data):
        renderer = self.get_renderer()
        rendered_data = renderer().render(data=data)
        return rendered_data

    def handle_exception(self, exc):
        exception_handler = self.settings.EXCEPTION_HANDLER

        context = self.get_exception_handler_context()
        response_data = exception_handler(exc, context)

        if response_data is None:
            response_data = {
                'detail': 'Internal server error.',
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        else:
            status_code = getattr(exc, 'status_code', None)
            if status_code is not None:
                response_data.update({'status': status_code})
        self.send_exception(response_data)

    def send_exception(self, response_data):
        raise NotImplementedError

    def dispatch(self, message, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(message, *args, **kwargs)
        self.request = request
        try:
            channel_name = request.channel.name
            if channel_name in self.channel_names:
                handler = getattr(self, self.channels_map[channel_name], self.not_allowed)
            else:
                handler = self.not_allowed
            handler(request, *args, **kwargs)
        except Exception as exc:
            self.handle_exception(exc)


class WebSocketView(BaseChannelsView):
    channel_names = ('websocket.connect', 'websocket.receive', 'websocket.disconnect')
    channels_map = {
        'websocket.connect': 'connect',
        'websocket.receive': 'receive',
        'websocket.disconnect': 'disconnect'
    }

    def send(self, channel_or_group, data, content_type='text', close=False):
        channel_or_group.send({content_type: self.get_rendered_data(data), 'close': close})

    def send_exception(self, response_data):
        self.send(self.request.reply_channel, response_data)


class EmailView(BaseChannelsView):
    channel_names = ('email.receive',)
    channels_map = {
        'email.receive': 'receive',
    }


class UDPView(BaseChannelsView):
    channel_names = ('udp.receive',)
    channels_map = {
        'udp.receive': 'receive',
    }


class HTTPView(BaseChannelsView):
    channel_names = ('http.request',)
    channels_map = {
        'http.request': 'receive'
    }

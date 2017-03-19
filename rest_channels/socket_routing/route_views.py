# coding=utf-8
from __future__ import unicode_literals

from channels.sessions import channel_session
from django.utils.decorators import method_decorator
from rest_framework import status as rest_framework_status

from rest_channels.socket_routing.serializers import RouteResponseSerializer, RouteSerializer
from rest_channels.views import WebSocketView


class SocketRouteView(WebSocketView):
    action = 'no_action'

    @method_decorator(channel_session)
    def receive(self, request, *args, **kwargs):
        serializer = RouteSerializer(data=request.data, context={'view': self})
        serializer.is_valid(raise_exception=True)
        method = serializer.data['method']
        self.action = method
        getattr(self, method)(request, serializer.data.get('data'), *args, **kwargs)

    def route_send(self, channel_or_group, data, status=rest_framework_status.HTTP_200_OK,
                   method=None, content_type='text', close=False):
        if method is None:
            method = self.action
        self.send(
            channel_or_group,
            RouteResponseSerializer({'data': data, 'status': status, 'method': method}).data,
            content_type,
            close
        )

    def handle_exception(self, exc):
        exception_handler = self.settings.EXCEPTION_HANDLER

        context = self.get_exception_handler_context()
        response_data = exception_handler(exc, context)

        if response_data is None:
            status_code = rest_framework_status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            status_code = getattr(
                exc,
                'status_code',
                rest_framework_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        self.route_send(
            self.request.reply_channel,
            data=response_data if response_data else {'detail': 'Internal server error.'},
            status=status_code
        )

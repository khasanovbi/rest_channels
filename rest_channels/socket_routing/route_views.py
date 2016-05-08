# coding=utf-8
from __future__ import unicode_literals

from channels.sessions import channel_session
from django.utils.decorators import method_decorator
from rest_framework import status as rest_framework_status

from rest_channels.socket_routing.serializers import RouteSerializer, RouteResponseSerializer
from rest_channels.views import SocketView


class SocketRouteView(SocketView):
    @method_decorator(channel_session)
    def receive(self, request, *args, **kwargs):
        serializer = RouteSerializer(data=request.data, context={'view': self})
        serializer.is_valid(raise_exception=True)
        method = serializer.data['method']
        self.action = method
        getattr(self, method)(request, serializer.data.get('data'), *args, **kwargs)

    def route_send(self, channel_or_group, data, method=None,
                   status=rest_framework_status.HTTP_200_OK, content_type='text', close=False):
        if method is None:
            assert self.action is not None
            method = self.action
        self.send(
            channel_or_group,
            RouteResponseSerializer({'data': data, 'status': status, 'method': method}).data,
            content_type,
            close
        )

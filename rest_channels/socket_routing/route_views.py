# coding=utf-8
from __future__ import unicode_literals

from channels.sessions import channel_session

from rest_channels.decorators import rest_channels
from rest_channels.socket_routing.serializers import RouteSerializer
from rest_channels.views import SocketView


class SocketRouteView(SocketView):
    @rest_channels(channel_session)
    def receive(self, request, *args, **kwargs):
        serializer = RouteSerializer(data=request.data, context={'view': self})
        serializer.is_valid(raise_exception=True)
        method = serializer.data['method']
        getattr(self, method)(request, serializer.data.get('data'), *args, **kwargs)

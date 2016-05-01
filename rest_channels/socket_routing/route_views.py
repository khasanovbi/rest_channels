# coding=utf-8
from __future__ import unicode_literals

from rest_channels.views import SocketView


class SocketRouteView(SocketView):
    @classmethod
    def as_view(cls, **initkwargs):
        pass

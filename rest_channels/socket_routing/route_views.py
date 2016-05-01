from rest_channels.views import SocketView


class SocketRouteView(SocketView):
    @classmethod
    def as_view(cls, **initkwargs):
        pass
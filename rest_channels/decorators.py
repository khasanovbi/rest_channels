# coding=utf-8
from __future__ import unicode_literals


def rest_channels(channels_func):
    # TODO: I need an idea to fix this decorator hell
    def inner1(rest_channels_func):
        def inner2(view, request, *args, **kwargs):
            def inner3(message, *args, **kwargs):
                return rest_channels_func(view, request, *args, **kwargs)

            channels_func(inner3)(request._message, *args, **kwargs)

        return inner2

    return inner1

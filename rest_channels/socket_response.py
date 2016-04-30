"""
The Response class in REST framework is similar to HTTPResponse, except that
it is initialized with unrendered data, instead of a pre-rendered string.

The appropriate renderer is called during Django's template response rendering.
"""
from __future__ import unicode_literals

from django.utils import six
from rest_framework.serializers import Serializer


class SocketResponse(object):
    def __init__(self, data=None, bytes_renderer=None,):
        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = data

    @property
    def rendered_content(self):
        renderer = getattr(self, 'accepted_renderer', None)
        media_type = getattr(self, 'accepted_media_type', None)
        context = getattr(self, 'renderer_context', None)

        assert renderer, ".accepted_renderer not set on Response"
        assert media_type, ".accepted_media_type not set on Response"
        assert context, ".renderer_context not set on Response"
        context['response'] = self

        charset = renderer.charset

        ret = renderer.render(self.data, media_type, context)
        if isinstance(ret, six.text_type):
            assert charset, (
                'renderer returned unicode, and did not specify '
                'a charset value.'
            )
            return bytes(ret.encode(charset))

        return ret

from __future__ import unicode_literals

import sys

import six


class Empty(object):
    """
    Placeholder for unset attributes.
    Cannot use `None`, as that may be a valid value.
    """
    pass


def _hasattr(obj, name):
    return not getattr(obj, name) is Empty


class ContentType(object):
    text = 'text'
    bytes = 'bytes'
    none = 'none'


class SocketRequest(object):
    def __init__(self, message, text_parser_class=None, bytes_parser_class=None):
        # TODO think more how to solve this hack more correct way
        self.__class__ = type(
            message.__class__.__name__,
            (self.__class__, message.__class__),
            {}
        )
        self._message = message
        self.text_parser_class = text_parser_class
        self.bytes_parser_class = bytes_parser_class
        self._text = Empty
        self._bytes = Empty
        self._full_data = Empty

    @property
    def content_type(self):
        if self._message.content.get(ContentType.text) is not None:
            return ContentType.text
        elif self._message.content.get(ContentType.bytes) is not None:
            return ContentType.bytes
        else:
            return ContentType.none

    @property
    def data(self):
        if not _hasattr(self, '_full_data'):
            self._load_text_and_bytes()
        return self._full_data

    def _load_text_and_bytes(self):
        """
        Parses the message content into `self.data`.
        """
        if not _hasattr(self, '_bytes'):
            self._text, self._bytes = self._parse()
            if self._bytes:
                self._full_data = self._text.copy()
                self._full_data.update(self._bytes)
            else:
                self._full_data = self._text

    def select_parser(self):
        if self.content_type == ContentType.text:
            return self.text_parser_class
        else:
            return self.bytes_parser_class

    def _parse(self):
        media_type = self.content_type
        parser = self.select_parser()
        if parser is not None:
            try:
                parsed = parser().parse(self._message.content.get(media_type))
                if media_type == ContentType.text:
                    return parsed, None
                elif media_type == ContentType.bytes:
                    return None, parsed
                else:
                    return None, None
            except:
                self._text = None
                self._bytes = None
                raise
        return None, None

    def __getattribute__(self, attr):
        """
        If an attribute does not exist on this instance, then we also attempt
        to proxy it to the underlying HttpRequest object.
        """
        try:
            return super(SocketRequest, self).__getattribute__(attr)
        except AttributeError:
            info = sys.exc_info()
            try:
                return getattr(self._message, attr)
            except AttributeError:
                six.reraise(info[0], info[1], info[2].tb_next)

    @property
    def TEXT(self):
        if not _hasattr(self, '_text'):
            self._load_text_and_bytes()
        return self._text

    @property
    def BYTES(self):
        if not _hasattr(self, '_bytes'):
            self._load_text_and_bytes()
        return self._bytes

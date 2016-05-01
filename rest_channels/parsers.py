# coding=utf-8
from __future__ import unicode_literals

import ujson
from rest_framework.compat import six
from rest_framework.exceptions import ParseError
from rest_framework.renderers import JSONRenderer


class BaseParser(object):
    def parse(self, data):
        """
        Given a stream to read from, return the parsed representation.
        Should return parsed data, or a `DataAndFiles` object consisting of the
        parsed data and files.
        """
        raise NotImplementedError(".parse() must be overridden.")


class UJSONParser(BaseParser):
    renderer_class = JSONRenderer

    def parse(self, data):
        try:
            return ujson.loads(data)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))

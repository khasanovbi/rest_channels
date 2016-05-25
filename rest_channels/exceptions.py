# coding=utf-8
from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from rest_framework import status


class ChannelsException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail)

    def __str__(self):
        return self.detail


class EventNotAllowed(ChannelsException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = _('Event "{event}" not allowed.')

    def __init__(self, event, detail=None):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail).format(event=event)

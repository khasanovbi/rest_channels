# coding=utf-8
from __future__ import unicode_literals


def socket_route(func):
    func.socket_route = True
    return func

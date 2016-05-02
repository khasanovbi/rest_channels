# coding=utf-8
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


# noinspection PyProtectedMember,PyAbstractClass
class RouteSerializer(serializers.Serializer):
    method = serializers.CharField()
    data = serializers.DictField()

    def validate_method(self, method_name):
        view = self.context['view']
        method = getattr(view, method_name, None)
        if method is None or not getattr(method, 'socket_route', None):
            raise ValidationError(
                'Method {method_name} not supplied'.format(method_name=method_name)
            )
        return method_name


# noinspection PyAbstractClass
class RouteResponseSerializer(RouteSerializer):
    status = serializers.IntegerField(min_value=100, max_value=600)

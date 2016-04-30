import ujson

import six


class BaseRenderer(object):
    def render(self, data):
        raise NotImplementedError('Renderer class requires .render() to be implemented')


class UJSONRenderer(BaseRenderer):
    def render(self, data, *args, **kwargs):
        if data is None:
            return ''
        ret = ujson.dumps(data)
        return ret

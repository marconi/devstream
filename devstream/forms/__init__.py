# -*- coding: utf-8 -*-

from formencode import Invalid
from formencode.variabledecode import variable_decode


class State(object):
    """
    Default "empty" state object.

    Keyword arguments are automatically bound to properties,
    for example::

        obj = State(foo="bar")
        obj.foo == "bar"
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __contains__(self, k):
        return hasattr(self, k)

    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError

    def __setitem__(self, k, v):
        setattr(self, k, v)

    def get(self, k, default=None):
        return getattr(self, k, default)


def validate_form(request, schema):
    """ Helper that validates posted
    fields against a formencode schema """
    params = variable_decode(request.POST)
    result = dict(data=None, errors=None)
    try:
        result['data'] = schema.to_python(params, State())
    except Invalid, e:
        result['errors'] = e.unpack_errors()
    return result

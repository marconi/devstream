# -*- coding: utf-8 -*-

from pyramid.events import BeforeRender, NewRequest, subscriber
from pyramid.i18n import get_localizer, TranslationStringFactory
from pyramid.httpexceptions import HTTPForbidden
from pyramid.exceptions import ConfigurationError

from devstream.lib import helpers

tsf = TranslationStringFactory('devstream')


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request = event.get('request')
    if request is None:
        request = get_current_request()

    globs = dict(h=helpers)

    if request is not None:
        globs['_'] = request.translate
        globs['localizer'] = request.localizer
        try:
            globs['session'] = request.session
        except ConfigurationError:
            pass

    def url(*args, **kwargs):
        """ route_url shorthand """
        return request.route_url(*args, **kwargs)

    globs['url'] = url
    event.update(globs)


@subscriber(NewRequest)
def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)

    def auto_translate(string, **kwargs):
        return localizer.translate(tsf(string, **kwargs))
    request.localizer = localizer
    request.translate = auto_translate


@subscriber(NewRequest)
def csrf_validation(event):
    if event.request.method == "POST":
        token = event.request.POST.get("_csrf", None)
        if token is None or token != event.request.session.get_csrf_token():
            raise HTTPForbidden("CSRF token is missing or invalid")
        elif token:
            # remove token after using it so
            # it doesn't get validated in formencode
            del event.request.POST['_csrf']

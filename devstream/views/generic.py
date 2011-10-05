# -*- coding: utf-8 -*-

import json
import logging
import redis
from json import loads, dumps

from pyramid.view import view_config
from pyramid.i18n import TranslationString as _
from pyramid.httpexceptions import HTTPFound, HTTPCreated, HTTPOk
from pyramid.httpexceptions import HTTPMethodNotAllowed, HTTPBadRequest
from pyramid.httpexceptions import HTTPForbidden

from devstream.forms.status import StatusSchema
from devstream.forms import validate_form
from devstream.models.status import Status

log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='home.mako')
def home(request):
    return dict(greetings="Hello World")


@view_config(route_name='post_status', request_method='POST',
             xhr=True, renderer='json')
def do_post_status(request):
    response = dict()
    result = validate_form(request, StatusSchema())
    if result['errors']:
        response.update(result['errors'])
        raise HTTPBadRequest(body=json.dumps(response))
    else:
        status = Status(status=result['data']['status'])
        status.save()
        response['message'] = _("Status successfully posted")

        # publish status to channel
        rdis = redis.Redis()
        msg = {'type': 'status', 'content': status.status}
        rdis.publish('devstream', dumps(msg))

        return HTTPOk(body=json.dumps(response))

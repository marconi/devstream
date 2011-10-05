# -*- coding: utf-8 -*-

from formencode import Invalid, Schema, validators

from pyramid.i18n import TranslationString as _


class StatusSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    status = validators.String(not_empty=True,
        messages={'empty': _('You need to enter a status')})

# -*- coding: utf-8 -*-

from mongoengine import *

from devstream.models.user import User


class Status(Document):
    status = StringField(required=True)
    owner = ReferenceField(User)

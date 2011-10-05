# -*- coding: utf-8 -*-

from mongoengine import *


class Status(Document):
    status = StringField(required=True)

# -*- coding: utf-8 -*-

import random
import hashlib
from datetime import datetime, timedelta
from flaskext.login import UserMixin

from devstream.extensions import db
from devstream import settings


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))
    is_activated = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now())

    owned_groups = db.relationship("Group", backref="owner")

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

    def is_active(self):
        return self.is_activated


class ActivationKey(db.Model):
    __tablename__ = 'activation_keys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref('activation_key',
                                                      uselist=False))
    is_activated = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user):
        if not self.key:
            sha1 = hashlib.sha1(repr(settings.SECRET_KEY) + user.email)
            self.key = sha1.hexdigest()
        self.user = user
        self.user_id = user.id

    def __repr__(self):
        return '<ActivationKey %r>' % self.user.email

    def is_expired(self):
        exp = settings.ACTIVATION_EXPIRATION
        expiration_date = self.created + timedelta(days=exp)
        if datetime.now() >= expiration_date:
            return True
        return False

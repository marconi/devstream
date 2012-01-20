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


class BaseKeyGenerator(object):
    def generate_key(self, to_digest):
        sha1 = hashlib.sha1(repr(settings.SECRET_KEY) + to_digest)
        return sha1.hexdigest()

    def is_expired(self):
        exp = settings.ACTIVATION_EXPIRATION
        expiration_date = self.created + timedelta(days=exp)
        if datetime.now() >= expiration_date:
            return True
        return False


class ActivationKey(db.Model, BaseKeyGenerator):
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
            self.key = self.generate_key(user.email)
        self.user = user

    def __repr__(self):
        return '<ActivationKey %r>' % self.user.email


class InvitationKey(db.Model, BaseKeyGenerator):
    __tablename__ = 'invitation_keys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship("Group", backref=db.backref('invites'))
    is_activated = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, email, group):
        if not self.key:
            self.key = self.generate_key("%s%s" % (email, group.name))
        self.group = group
        self.email = email

    def __repr__(self):
        return '<InvitationKey %r>' % self.email

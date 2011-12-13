# -*- coding: utf-8 -*-

import random
import hashlib
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from devstream.libs.database import Base
from devstream import settings


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    username = Column(String(50))
    password = Column(String(80))
    is_active = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email


class ActivationKey(Base):
    __tablename__ = 'activation_keys'
    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref('activation_key',
                                                uselist=False))
    is_activated = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now())

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

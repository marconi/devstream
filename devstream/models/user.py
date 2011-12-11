# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from devstream.libs.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    username = Column(String(50))
    password = Column(String(80))
    is_active = Column(Boolean, default=False)
    created = Column(DateTime)

    def __init__(self, email, password):
        if self.created is None:
            self.created = datetime.now()
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from devstream.libs.database import Base


class Status(Base):
    __tablename__ = 'statuses'
    id = Column(Integer, primary_key=True)
    status = Column(String(255))
    type = Column(Enum('STATUS', 'GIT', name='status_types'))
    created = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref('statuses'))

    def __init__(self, status, type, user=None):
        if self.created is None:
            self.created = datetime.utcnow()
        if user:
            self.user = user
        self.status = status
        self.type = type

    def __repr__(self):
        return '<Status %r>' % self.status

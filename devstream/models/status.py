# -*- coding: utf-8 -*-

# from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
# from sqlalchemy.orm import relationship, backref
from datetime import datetime

from devstream.extensions import db



class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    type = db.Column(db.Enum('STATUS', 'GIT', name='status_types'))
    created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref('statuses'))

    def __init__(self, status, user=None, type='STATUS'):
        self.user = user
        self.status = status
        self.type = type

    def __repr__(self):
        return '<Status %r>' % self.status

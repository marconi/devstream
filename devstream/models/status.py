# -*- coding: utf-8 -*-

from datetime import datetime

from devstream.extensions import db



class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    type = db.Column(db.Enum('STATUS', 'GIT', name='status_types'))
    created = db.Column(db.DateTime, default=datetime.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship("User", backref=db.backref('statuses'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __init__(self, status, group_id, owner=None, type='STATUS'):
        self.group_id = group_id
        self.owner = owner
        self.status = status
        self.type = type

    def __repr__(self):
        return '<Status %r>' % self.status

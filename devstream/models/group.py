# -*- coding: utf-8 -*-

from datetime import datetime

from devstream.extensions import db


memberships_association = db.Table('group_memberships', db.metadata,
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    members = db.relationship("User",
                              secondary=memberships_association,
                              backref=db.backref('groups'))
    stream = db.relationship("Status", backref=db.backref('group'))

    def __init__(self, name, user=None):
        self.name = name
        self.user = user

    def last_activity(self):
        """ Return the timestamp from last group activity. """
        return None

    def get_members_count(self):
        """ Return all members of this group. """
        return 0

    def __repr__(self):
        return '<Group %r>' % self.name

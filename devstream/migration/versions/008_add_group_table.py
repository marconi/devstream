from datetime import datetime

from sqlalchemy import *
from migrate import *

from devstream.extensions import db


DeclarativeBase = db.make_declarative_base()

memberships_association = db.Table('group_memberships', DeclarativeBase.metadata,
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class User(DeclarativeBase):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # ...


class Group(DeclarativeBase):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    members = db.relationship("User",
                              secondary=memberships_association,
                              backref=db.backref('groups'))

def upgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    Group.__table__.create()
    memberships_association.create()


def downgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    memberships_association.drop()
    Group.__table__.drop()

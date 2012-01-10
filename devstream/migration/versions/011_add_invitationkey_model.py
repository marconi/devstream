from datetime import datetime

from sqlalchemy import *
from migrate import *

from devstream.extensions import db


DeclarativeBase = db.make_declarative_base()

class Group(DeclarativeBase):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    # ...


class InvitationKey(DeclarativeBase):
    __tablename__ = 'invitation_keys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship("Group", backref=db.backref('invites'))
    is_activated = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now())


def upgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    InvitationKey.__table__.create()


def downgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    InvitationKey.__table__.drop()

from datetime import datetime

from sqlalchemy import *
from migrate import *
from migrate.changeset import create_column, drop_column

from devstream.extensions import db


DeclarativeBase = db.make_declarative_base()

class Group(DeclarativeBase):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    # ...


class Status(DeclarativeBase):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    # ...
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))


def upgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    create_column(Status.__table__.c.group_id, table=Status.__table__)


def downgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    drop_column(Status.__table__.c.group_id, table=Status.__table__)

from sqlalchemy import *
from migrate import *

from devstream.extensions import db


DeclarativeBase = db.make_declarative_base()

class User(DeclarativeBase):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # ...


class Status(DeclarativeBase):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    type = db.Column(db.Enum('STATUS', 'GIT', name='status_types'))
    created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref('statuses'))


def upgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    Status.__table__.create()


def downgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    Status.__table__.drop()

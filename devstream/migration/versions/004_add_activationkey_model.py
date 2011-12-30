from datetime import datetime

from sqlalchemy import *
from migrate import *

from devstream.extensions import db


DeclarativeBase = db.make_declarative_base()

class User(DeclarativeBase):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    created = db.Column(db.DateTime, default=datetime.now())
    username = db.Column(db.String(50))


class ActivationKey(DeclarativeBase):
    __tablename__ = 'activation_keys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref('activation_key',
                                                      uselist=False))
    created = db.Column(db.DateTime, default=datetime.now())


def upgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    ActivationKey.__table__.create()


def downgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    ActivationKey.__table__.drop()

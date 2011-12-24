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


def upgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    User.__table__.create()


def downgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    User.__table__.drop()

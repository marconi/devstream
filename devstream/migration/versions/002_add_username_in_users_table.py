from sqlalchemy import *
from migrate import *
from migrate.changeset import create_column, drop_column

from devstream.extensions import db
from devstream.models import User


DeclarativeBase = db.make_declarative_base()

class User(DeclarativeBase):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # ...
    username = db.Column(db.String(50))


def upgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    create_column(User.__table__.c.username, table=User.__table__)


def downgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    drop_column(User.__table__.c.username, table=User.__table__)

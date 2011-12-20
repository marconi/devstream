from sqlalchemy import *
from migrate import *
from migrate.changeset import create_column, drop_column

from devstream.extensions import db


DeclarativeBase = db.make_declarative_base()

class ActivationKey(DeclarativeBase):
    __tablename__ = 'activation_keys'
    id = db.Column(db.Integer, primary_key=True)
    # ...
    is_activated = db.Column(db.Boolean, default=False)


def upgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    create_column(ActivationKey.__table__.c.is_activated,
                  table=ActivationKey.__table__)


def downgrade(migrate_engine):
    metadata = DeclarativeBase.metadata
    metadata.bind = migrate_engine
    drop_column(ActivationKey.__table__.c.is_activated,
                table=ActivationKey.__table__)

from sqlalchemy import *
from migrate import *

from devstream.extensions import db
from devstream.models import ActivationKey


def upgrade(migrate_engine):
    db.metadata.bind = migrate_engine
    ActivationKey.__table__.create()


def downgrade(migrate_engine):
    db.metadata.bind = migrate_engine
    ActivationKey.__table__.drop()

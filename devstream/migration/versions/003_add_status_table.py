from sqlalchemy import *
from migrate import *

from devstream.libs.database import metadata
from devstream.models import Status


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    Status.__table__.create()


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    Status.__table__.drop()

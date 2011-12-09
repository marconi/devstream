from sqlalchemy import *
from migrate import *

from devstream.libs.database import metadata
from devstream.models import User


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    User.__table__.create()


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    User.__table__.drop()

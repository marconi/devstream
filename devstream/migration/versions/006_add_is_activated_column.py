from sqlalchemy import *
from migrate import *
from migrate.changeset import create_column, drop_column

from devstream.libs.database import metadata
from devstream.models import ActivationKey


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    create_column(ActivationKey.__table__.c.is_activated,
                  table=ActivationKey.__table__)


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    drop_column(ActivationKey.__table__.c.is_activated,
                table=ActivationKey.__table__)

from sqlalchemy import *
from migrate import *
from migrate.changeset import create_column, drop_column
import transaction

from devstream.extensions import db


def upgrade(migrate_engine):
    db.metadata.bind = migrate_engine
    sql = "ALTER TABLE users RENAME COLUMN is_active to is_activated"
    migrate_engine.execute(sql)
    transaction.commit()


def downgrade(migrate_engine):
    db.metadata.bind = migrate_engine
    sql = "ALTER TABLE users RENAME COLUMN is_activated to is_active"
    migrate_engine.execute(sql)
    transaction.commit()

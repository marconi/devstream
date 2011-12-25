from sqlalchemy import *
from migrate import *
import transaction

from devstream.extensions import db


def upgrade(migrate_engine):
    db.metadata.bind = migrate_engine
    sql = "ALTER TABLE statuses RENAME COLUMN user_id to owner_id"
    migrate_engine.execute(sql)
    transaction.commit()


def downgrade(migrate_engine):
    db.metadata.bind = migrate_engine
    sql = "ALTER TABLE statuses RENAME COLUMN owner_id to user_id"
    migrate_engine.execute(sql)
    transaction.commit()

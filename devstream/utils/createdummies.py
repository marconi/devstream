# -*- coding: utf-8 -*-

from devstream.libs.database import db_session
from devstream.models import User, Status


user1 = User('user1@gmail.com', 'randompass')
user2 = User('user2@gmail.com', 'randompass')

db_session.add(user1)
db_session.add(user2)
db_session.commit()


status1 = Status('Hello', 'STATUS', user1)
db_session.add(status1)
db_session.commit()

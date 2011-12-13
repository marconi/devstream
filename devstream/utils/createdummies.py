# -*- coding: utf-8 -*-

from devstream.extensions import db
from devstream.models import User, Status


user1 = User('user1@gmail.com', 'randompass')
user2 = User('user2@gmail.com', 'randompass')

db.session.add(user1)
db.session.add(user2)
db.session.commit()


status1 = Status('Hello', 'STATUS', user1)
db.session.add(status1)
db.session.commit()

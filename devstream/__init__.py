# -*- coding: utf-8 -*-

import os
from flask import Flask
from flaskext.babel import Babel
from flaskext.mail import Mail

from devstream.libs.database import db_session


app = Flask(__name__)
app.config.from_object('devstream.settings')

# load extensions
babel = Babel(app)
mail = Mail(app)

# hooks
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# discover views
from devstream.views import *

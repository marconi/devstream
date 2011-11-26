# -*- coding: utf-8 -*-

import os
from flask import Flask
from flaskext.babel import Babel


app = Flask(__name__)
app.config.from_object('devstream.settings')
babel = Babel(app)

from devstream.views import *

# -*- coding: utf-8 -*-

from flaskext.babel import Babel
from flaskext.mail import Mail
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.login import LoginManager


__all__ = ['babel', 'mail', 'db', 'login_manager']

# load extensions
babel = Babel()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()

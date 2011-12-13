# -*- coding: utf-8 -*-

from flaskext.babel import Babel
from flaskext.mail import Mail
from flaskext.sqlalchemy import SQLAlchemy


__all__ = ['babel', 'mail', 'db']

# load extensions
babel = Babel()
mail = Mail()
db = SQLAlchemy()

# -*- coding: utf-8 -*-

from flaskext.babel import Babel
from flaskext.mail import Mail


__all__ = ['babel', 'mail', 'jsonify']

# load extensions
babel = Babel()
mail = Mail()

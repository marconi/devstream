# -*- coding: utf-8 -*-

import os


PROJEC_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = '\xb0\x03\xc7nY\x0c\x91X\xb1\x87-=\x0b\x19\xf3w\x0c5@o\xc8\xdf\xfft'
DATABASE_NAME = 'devstream'
DATABASE_URI_PREFIX = 'postgresql://postgres:postgres@localhost'
SQLALCHEMY_DATABASE_URI = '%s/%s' % (DATABASE_URI_PREFIX, DATABASE_NAME)

# wtforms settings
CSRF_ENABLED = True

# Flask-Mail settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None
DEFAULT_MAIL_SENDER = 'noreply@devstream.com'

# custom settings
TEST_DATABASE_NAME = 'devstream_test'
SITE_NAME = 'DevStream'
SITE_DOMAIN_NAME = 'devstream.com'

DEFAULT_STREAM_ITEMS = 10
DEFAULT_SHOW_MORE_ITEMS = 5

ACTIVATION_EXPIRATION = 1

try:
    from local_settings import *
except ImportError:
    pass

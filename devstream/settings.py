# -*- coding: utf-8 -*-

import os


PROJEC_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = '\xb0\x03\xc7nY\x0c\x91X\xb1\x87-=\x0b\x19\xf3w\x0c5@o\xc8\xdf\xfft'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/devstream'


# custom settings
DEFAULT_STREAM_ITEMS = 10
DEFAULT_SHOW_MORE_ITEMS = 5

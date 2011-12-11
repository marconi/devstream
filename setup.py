# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


requires = ['Flask', 'flask-jsonify', 'SQLAlchemy', 'sqlalchemy-migrate',
            'Babel', 'psycopg2', 'Flask-WTF', 'cryptacular', 'Flask-Mail']

setup(name='devstream',
      version='0.1',
      description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Marconi Moreto',
      author_email='caketoad@gmail.com',
      url='',
      keywords='web collaboration flask',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
)

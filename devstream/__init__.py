# -*- coding: utf-8 -*-

import threading
from flask import Flask

from devstream.extensions import babel, mail, db, login_manager
from devstream.views.status import status
from devstream.views.common import common
from devstream.views.dashboard import dashboard
from devstream.models import User
from devstream.forms.generic import LoginForm
from devstream.libs.roster import _run_roster


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('devstream.settings')

    # configure extensions
    babel.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.setup_app(app)
    login_manager.login_view = "common.login"

    # register blueprints
    app.register_blueprint(status)
    app.register_blueprint(common)
    app.register_blueprint(dashboard)

    initialize_contexts(app)

    # spawn the roster thread to monitor roster activities
    roster_thread = threading.Thread(target=_run_roster, args=(app,))
    roster_thread.setDaemon(True)
    roster_thread.start()

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def initialize_contexts(app):
    """ Context initializer. Wraps context
    functions on context_processor  decorator. """
    app.context_processor(add_forms)


def add_forms():
    login_form = LoginForm()
    return dict(login_form=login_form)

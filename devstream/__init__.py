# -*- coding: utf-8 -*-

from flask import Flask


from devstream.libs.database import db_session
from devstream.extensions import babel, mail
from devstream.views.status import status
from devstream.views.common import common


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('devstream.settings')

    # hooks
    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()

    # configure extensions
    babel.init_app(app)
    mail.init_app(app)

    # register blueprints
    app.register_blueprint(status)
    app.register_blueprint(common)

    return app

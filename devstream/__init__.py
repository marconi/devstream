from mongoengine import connect

from pyramid.config import Configurator
from pyramid.events import NewRequest, subscriber
from pyramid_beaker import session_factory_from_settings

from devstream.resources import Root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_static_view('static', 'devstream:static')

    # init beaker session
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # connect to mongodb
    connect(settings.get('mongodb.db', 'test'),
            host=settings.get('mongodb.host', 'localhost'),
            port=int(settings.get('mongodb.port', 27017)))

    # includes
    config.include('devstream.views.add_routes')

    config.scan(package='devstream.lib')
    config.scan(package='devstream.views')
    return config.make_wsgi_app()

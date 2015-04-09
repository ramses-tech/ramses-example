from pyramid.config import Configurator
from wsgiref.simple_server import make_server


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()

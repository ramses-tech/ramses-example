from pyramid.config import Configurator
from ramses import registry


@registry.add
def user_himself(ace, request, obj):
    from pyramid.security import Allow
    return [
        (Allow, str(obj.id), 'patch'),
        (Allow, str(obj.username), 'patch'),
    ]


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()

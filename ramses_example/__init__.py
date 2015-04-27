from pyramid.config import Configurator
from ramses import registry


@registry.add
def user_self(ace, request, obj):
    """ Give 'patch' permission to user when trying to edit itself. """
    from pyramid.security import Allow
    user = getattr(request, 'user', None)
    if user is not None and user.username == obj.username:
        return [
            (Allow, str(user.id), 'patch'),
            (Allow, str(user.username), 'patch'),
        ]


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()

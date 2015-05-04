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


@registry.add
def lower_strip_processor(value):
    return (value or '').lower().strip()


@registry.add
def crypt_processor(value):
    """ Crypt :value: if it's not crypted yet """
    import cryptacular.bcrypt
    crypt = cryptacular.bcrypt.BCRYPTPasswordManager()
    if value and not crypt.match(value):
        value = unicode(crypt.encode(value))
    return value


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()

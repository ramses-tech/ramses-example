import logging

from pyramid.config import Configurator
from ramses import registry

log = logging.getLogger(__name__)


def my_is_admin(cls, user):
    """ Example of overriding  """
    log.info('Checking if user {} is admin'.format(user))
    return 'admin' in user.groups
registry.add('User.is_admin', classmethod(my_is_admin))


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
def lower_strip_processor(instance, new_value):
    if new_value is None:
        return new_value
    return new_value.lower().strip()


@registry.add
def crypt_processor(instance, new_value):
    """ Crypt :new_value: if it's not crypted yet """
    import cryptacular.bcrypt
    crypt = cryptacular.bcrypt.BCRYPTPasswordManager()
    if new_value and not crypt.match(new_value):
        new_value = str(crypt.encode(new_value))
    return new_value


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()

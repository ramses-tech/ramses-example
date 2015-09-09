import logging

from pyramid.config import Configurator
from ramses import registry

log = logging.getLogger(__name__)


def my_is_admin(cls, user):
    """ Example of overriding """
    log.info('Checking if user {} is admin'.format(user))
    return 'admin' in user.groups
registry.add('User.is_admin', classmethod(my_is_admin))


@registry.add
def user_self(ace, request, obj):
    """ Give 'update' permission to user that is being created. """
    from pyramid.security import Allow
    return [(Allow, str(obj.username), 'update')]


@registry.add
def lower_strip_processor(**kwargs):
    """ Make :new_value: lowercase (and stripped) """
    new_value = kwargs['new_value']
    if new_value is None:
        return new_value
    return new_value.lower().strip()


@registry.add
def crypt_processor(**kwargs):
    """ Crypt :new_value: if it's not crypted yet """
    import cryptacular.bcrypt
    new_value = kwargs['new_value']
    field = kwargs['field']
    min_length = field.params['min_length']
    if len(new_value) < min_length:
        raise ValueError(
            '`{}`: Value length must be more than {}'.format(
                field.name, field.params['min_length']))

    crypt = cryptacular.bcrypt.BCRYPTPasswordManager()
    if new_value and not crypt.match(new_value):
        new_value = str(crypt.encode(new_value))
    return new_value


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()

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
    """ Give 'patch' permission to user when trying to edit itself """
    from pyramid.security import Allow
    user = getattr(request, 'user', None)
    if user is not None and user.username == obj.username:
        return [
            (Allow, str(user.username), 'patch'),
        ]


@registry.add
def lower_strip_processor(event):
    """ Make :new_value: lowercase (and stripped) """
    value = (event.field.new_value or '').lower().strip()
    event.set_field_value(value)


@registry.add
def crypt_processor(event):
    """ Crypt :new_value: if it's not crypted yet """
    import cryptacular.bcrypt
    field = event.field
    new_value = field.new_value
    min_length = field.params['min_length']
    if len(new_value) < min_length:
        raise ValueError(
            '`{}`: Value length must be more than {}'.format(
                field.name, field.params['min_length']))

    crypt = cryptacular.bcrypt.BCRYPTPasswordManager()
    if new_value and not crypt.match(new_value):
        encrypted = str(crypt.encode(new_value))
        field.new_value = encrypted
        event.set_field_value(encrypted)


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()

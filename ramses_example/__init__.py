import logging

from dateutil import parser as dtparser
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
    return (new_value or '').lower().strip()


@registry.add
def crypt_processor(instance, new_value):
    """ Crypt :new_value: if it's not crypted yet """
    import cryptacular.bcrypt
    crypt = cryptacular.bcrypt.BCRYPTPasswordManager()
    if new_value and not crypt.match(new_value):
        new_value = unicode(crypt.encode(new_value))
    return new_value


"""
Processors:
  :calculate_days: Is called for 'days' field and returns calculated date
    that will be set as new value for field in BaseDocument.clean method.
    When no processing is needed, passed 'new_value' must be returned
    (or instance.days). Contains a lot of dates convertions and
    calculations.

  :calculate_days_indirect: Is called for 'due_date' and 'start_date' fields.
    It is separate from 'calculate_days', because it does not need to modify
    value passed to it and needs to return value as is and 'calculate_days'
    actually need to return modified value.


How it works:

When 'days' field is changed:
'', None  =>  42:         'days' is set to 42
'', None  =>  '', None    'days' is calculated
42        =>  '', None    'days' is calculated
42        =>  11          'days' is set to 11

When 'due_date' or 'start_date' fields are changed they force
recalculation of 'days' field, no matter if 'days' field has value or not.

Days calculation from 'start_date' and 'due_date' only starts if both fields
have values.
"""


@registry.add
def calculate_days(instance, new_value, force_recalculate=False):
    current_days = instance.days
    days_not_empty = current_days != '' and current_days is not None

    # Everything is OK. Return field value
    if days_not_empty and not force_recalculate:
        return current_days

    # Get and parse dates if needed
    start_date = instance.start_date
    due_date = instance.due_date
    if not (start_date and due_date):
        return current_days
    if isinstance(start_date, basestring):
        start_date = dtparser.parse(start_date)
    if isinstance(due_date, basestring):
        due_date = dtparser.parse(due_date)
    due_date = due_date.replace(tzinfo=None)
    start_date = start_date.replace(tzinfo=None)

    return (due_date - start_date).days


@registry.add
def calculate_days_indirect(instance, new_value):
    days = calculate_days(instance, new_value, force_recalculate=True)
    instance.days = days
    return new_value


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()

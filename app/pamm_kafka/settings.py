from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# Make sure settings are installed
try:
    _ = settings.PAMM_KAFKA
except AttributeError:
    raise ImproperlyConfigured('Please define `PAMM_KAFKA` in your settings.py file.')


def get(key, default=None):
    if default is None and key not in settings.PAMM_KAFKA:
        raise ImproperlyConfigured('Please ensure PAMM_KAFKA["%s"] is defined in your settings.py file.' % key)
    return settings.PAMM_KAFKA.get(key, default)

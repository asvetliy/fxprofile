from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appdata',
        'USER': 'root',
        'PASSWORD': '123qweasd',
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': '3306',
    }
}

STATIC_ROOT = '/home/pyuser/app_data/public'
MEDIA_ROOT = '/home/pyuser/app_data/media'

EMAIL_HOST = '127.0.0.1'
EMAIL_USE_TLS = False
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply@xyz.trading'
EMAIL_HOST_PASSWORD = 's5l^Ab06'

ADMINS = [('Administrator', 'admin@xyz.trading')]
MANAGERS = ['support@xyz.trading']
DEFAULT_FROM_EMAIL = 'XYZ.TRADING <noreply@xyz.trading>'

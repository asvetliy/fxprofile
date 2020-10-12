from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fxprofile',
        'USER': 'fxprofile_sdfmkg',
        'PASSWORD': 'O4?36acb',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_ROOT = '/var/www/vhosts/xyz.trading/ca.xyz.trading/public'
MEDIA_ROOT = '/var/www/vhosts/xyz.trading/ca.xyz.trading/media'

EMAIL_HOST = '127.0.0.1'
EMAIL_USE_TLS = False
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply@xyz.trading'
EMAIL_HOST_PASSWORD = 's5l^Ab06'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'htc.fail.hell@gmail.com'
# EMAIL_HOST_PASSWORD = 'b4c5fail00!'

ADMINS = [('Administrator', 'admin@xyz.trading')]
MANAGERS = [('Support', 'support@xyz.trading')]
DEFAULT_FROM_EMAIL = 'noreply@xyz.trading'

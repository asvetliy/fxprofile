from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fxprofile',
        'USER': 'fxprofile_sdfmkg',
        'PASSWORD': 'O4?36acb',
        'HOST': '95.217.45.248',
        'PORT': '3306',
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'htc.fail.hell@gmail.com'
EMAIL_HOST_PASSWORD = 'b4c5fail00!'

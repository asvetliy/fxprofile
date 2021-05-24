from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appdata',
        'USER': 'root',
        'PASSWORD': os.environ.get('SQL_PASSWORD', '123qweasd'),
        'HOST': os.environ.get('SQL_HOST', '0.0.0.0'),
        'PORT': '3306',
    }
}


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'htc.fail.hell@gmail.com'
EMAIL_HOST_PASSWORD = 'b4c5fail00!'

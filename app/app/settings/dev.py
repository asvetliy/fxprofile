from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appdata',
        'USER': 'root',
        'PASSWORD': 'kA8rZ2cH2qW4oK7uK1uQ5aV5iX0nX7fK',
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': '3306',
    }
}


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'htc.fail.hell@gmail.com'
EMAIL_HOST_PASSWORD = 'b4c5fail00!'

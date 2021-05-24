"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zhjk&(*tk26uf#04ftpf&6fae=)f0lkr-6h)&^vf-c@3&lj&4d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fxprofile.apps.FxprofileConfig',
    'users.apps.UsersConfig',
    'mailer.apps.MailerConfig',
    'currency.apps.CurrencyConfig',
    'payment.apps.PaymentConfig',
    'verification.apps.VerificationConfig',
    'wallet.apps.WalletConfig',
    'wallet.templatetags.custom_filters',
    'mt4.apps.Mt4Config',
    'questions.apps.QuestionsConfig',
    'django_countries',
    'snowpenguin.django.recaptcha2',
    'json_logging.apps.JsonLoggingConfig',
    'pamm_kafka.apps.PammKafkaConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'json_logging.middleware.DjangoLoggingMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n'
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

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


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LOGIN_URL = reverse_lazy('user-login')
LOGIN_REDIRECT_URL = reverse_lazy('profile-index')
LOGOUT_REDIRECT_URL = reverse_lazy('user-login')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

RECAPTCHA_PRIVATE_KEY = '6Lc5AuAUAAAAAAohDU92CxZIe6RFKf5mx87SVrl1'
RECAPTCHA_PUBLIC_KEY = '6Lc5AuAUAAAAANo2eJX2gfhTKl-S1TGyU9lIup8R'
RECAPTCHA_LOGIN_FAILED_TRIES = 3
# Site key: 6Lc5AuAUAAAAANo2eJX2gfhTKl-S1TGyU9lIup8R
# Secret key: 6Lc5AuAUAAAAAAohDU92CxZIe6RFKf5mx87SVrl1

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/public/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
MEDIA_FILES_EXT = ['.pdf', '.jpeg', '.jpg', '.png', ]

MEDIA_MAX_FILESIZE = 5  # in MB

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CURRENCY_MODEL = 'currency.Currency'
AUTH_USER_MODEL = 'users.User'

handler404 = 'fxprofile.errors.ErrorView404'
handler500 = 'fxprofile.errors.ErrorView500'

MESSAGE_TAGS = {
    message_constants.DEBUG: 'alert alert-primary',
    message_constants.INFO: 'alert alert-info',
    message_constants.SUCCESS: 'alert alert-success',
    message_constants.WARNING: 'alert alert-warning',
    message_constants.ERROR: 'alert alert-danger',
}

MT4_HOST = '94.130.114.222'
MT4_PORT = 443
MT4_MASTER_PWD = 'JDhe4DCf4DdO'
MT4_MASTER_BALANCE_PWD = 'hLi7LuSuOIlYOg9'
MT4_ACCOUNTS_SETTINGS = {
    'MT4_REAL': {
        'FROM': 330000,
        'TO': 29000000,
        'STEP': 7,
        'GROUPS': {
            1: {
                1: '3',  # UGBN4
                2: '5',  # UGMN4
                3: '12'  # UGSN4
            },
            2: {
                1: '4',  # EGBN4
                2: '6',  # EGMN4
                3: '13'  # EGSN4
            }
        }
    }
}

# django-logging-json
DJANGO_LOGGING = {
    'LOG_LEVEL': 'info',
    'INDENT_CONSOLE_LOG': None,
    'CONSOLE_LOG': True,
}

PAMM_KAFKA = {
    # Required Settings
    'OFFSET_BACKEND': 'pamm_kafka.backend.kafka.ModelOffsetStore',
    'CONSUMER_BACKEND': 'pamm_kafka.backend.kafka.Consumer',
    'KAFKA_BOOTSTRAP_SERVERS': [
        'kafka.xyz.test:9092'
    ],
    'KAFKA_CONSUMER_KWARGS': {
        'group_id': 'fxprofile-pamm',
        'security_protocol': 'SASL_SSL',
        'sasl_mechanism': os.getenv('DJANGO_LOGPIPE_CONSUMER_SASL_MECHANISM', 'PLAIN'),
        'sasl_plain_username': os.getenv('DJANGO_LOGPIPE_CONSUMER_SASL_USERNAME', 'client'),
        'sasl_plain_password': os.getenv('DJANGO_LOGPIPE_CONSUMER_SASL_PASSWORD', ''),
        'ssl_cafile': os.getenv('DJANGO_LOGPIPE_CONSUMER_SSL_CA', ''),
        'ssl_certfile': os.getenv('DJANGO_LOGPIPE_CONSUMER_SSL_CERT', ''),
        'ssl_keyfile': os.getenv('DJANGO_LOGPIPE_CONSUMER_SSL_KEY', ''),
        'ssl_password': os.getenv('DJANGO_LOGPIPE_CONSUMER_SSL_PASSWORD', ''),
    },

    # Optional Settings
    # 'KAFKA_SEND_TIMEOUT': 10,
    # 'KAFKA_MAX_SEND_RETRIES': 0,
    'MIN_MESSAGE_LAG_MS': 0,
    'DEFAULT_FORMAT': 'json',
}
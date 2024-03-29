import logging
import logging.config
import os
import sys

from . import settings

LOG_LEVEL = settings.LOG_LEVEL.upper()
LOG_HANDLERS = ['default']

if settings.CONSOLE_LOG:
    LOG_HANDLERS.append('console')
if settings.DEBUG:
    LOG_HANDLERS.append('debug')
if settings.SQL_LOG:
    LOG_HANDLERS.append('sql')

if not os.path.exists(settings.LOG_PATH):
    try:
        os.makedirs(settings.LOG_PATH)
    except Exception as e:
        raise Exception(f"Unable to configure logger. Can't create LOG_PATH: {settings.LOG_PATH}")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': settings.DISABLE_EXISTING_LOGGERS,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s - %(created)s] file:%(module)s.py, func:%(funcName)s, ln:%(lineno)s: %(message)s',
        },
        'simple': {
            'format': '%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'sql': {
            'format': '[%(levelname)s - %(created)s] %(duration)s %(sql)s %(params)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'json_logging.handlers.ConsoleHandler',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
        'default': {
            'level': 'INFO',
            'class': 'json_logging.handlers.DefaultFileHandler',
            'formatter': 'verbose',
            'maxBytes': settings.ROTATE_MB * 1024 * 1024,
            'backupCount': settings.ROTATE_COUNT,
            'filename': f'{settings.LOG_PATH}/app.log',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'json_logging.handlers.DebugFileHandler',
            'formatter': 'verbose',
            'maxBytes': settings.ROTATE_MB * 1024 * 1024,
            'backupCount': settings.ROTATE_COUNT,
            'filename': f'{settings.LOG_PATH}/debug.log',
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'json_logging.handlers.SQLFileHandler',
            'formatter': 'sql',
            'maxBytes': settings.ROTATE_MB * 1024 * 1024,
            'backupCount': settings.ROTATE_COUNT,
            'filename': f'{settings.LOG_PATH}/sql.log',
        }
    },
    'loggers': {
        'dl_logger': {
            'handlers': LOG_HANDLERS,
            'level': LOG_LEVEL,
            'propagate': True,
        },
    }
}
logging.config.dictConfig(LOGGING)


def get_logger():
    logger = logging.getLogger('dl_logger')
    logger.setLevel(LOG_LEVEL)
    return logger

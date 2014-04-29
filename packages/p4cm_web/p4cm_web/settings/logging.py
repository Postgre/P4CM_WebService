from os.path import join, normpath

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
from django.conf import settings

LOG_ROOT = getattr(settings, 'LOG_ROOT', "")

PRJ_NAME = getattr(settings, 'PROJECT_NAME', "")

if PRJ_NAME:
    PRJ_LOG_ROOT = normpath(join(LOG_ROOT, PRJ_NAME))
else:
    PRJ_LOG_ROOT = LOG_ROOT


class LevelFilter(object):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        if self.level == record.levelname:
            return 1
        return 0


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] [logger: %(name)s] [line %(lineno)s, in %(module)s::%(funcName)s] %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'standard': {
            'format': "[%(asctime)s] [%(levelname)s] %(name)s[%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'OnlyDebug': {
            '()': LevelFilter,
            'level': 'DEBUG'
        },
        'OnlyInfo': {
            '()': LevelFilter,
            'level': 'INFO'
        },
        'OnlyWarning': {
            '()': LevelFilter,
            'level': 'WARNING'
        },
        'OnlyError': {
            '()': LevelFilter,
            'level': 'ERROR'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            #'filename' : os.path.join('/var/log/atrr', 'all.log'),
            'filename': normpath(join(PRJ_LOG_ROOT, 'all.log')),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'debug_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': normpath(join(PRJ_LOG_ROOT, 'debug.log')),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'verbose',
            'filters': ['OnlyDebug']
        },
        'info_log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': normpath(join(PRJ_LOG_ROOT, 'info.log')),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
            'filters': ['OnlyInfo']
        },
        'warn_log_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': normpath(join(PRJ_LOG_ROOT, 'warning.log')),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
            'filters': ['OnlyWarning']
        },
        'error_log_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': normpath(join(PRJ_LOG_ROOT, 'error.log')),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
            'filters': ['OnlyError']
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'p4cm_web': {
            'handlers': ['logfile', 'console', 'debug_log_file', 'info_log_file', 'warn_log_file', 'error_log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'util': {
            'handlers': ['logfile', 'console', 'debug_log_file', 'info_log_file', 'warn_log_file', 'error_log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION


"""Production settings and globals."""

import ConfigParser
from os import environ

from p4cm_web.p4cm_web.settings.base import *


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION

########## DATABASE CONFIGURATION
config = ConfigParser.ConfigParser()

config.readfp(open(APP_INST_CONFIG_FILE))

PROJECT_NAME = get_env_variable('project_name')
db_engine = 'django.db.backends.mysql'
db_host = config.get(PROJECT_NAME, 'db_host')
db_port = config.get(PROJECT_NAME, 'db_port')
db_name = config.get(PROJECT_NAME, 'db_name')
db_user = config.get(PROJECT_NAME, 'db_user')
db_password = config.get(PROJECT_NAME, 'db_password')

DATABASES = {
    'default': {
        'ENGINE': db_engine,
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
########################
###Cache Machine
########################
CACHES = {
    'default': dict(
        BACKEND='johnny.backends.memcached.MemcachedCache',
        LOCATION=['127.0.0.1:11211'],
        JOHNNY_CACHE=True,
    )
}
JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_atrr_%s' % PROJECT_NAME
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
#SECRET_KEY = get_env_variable('SECRET_KEY')
########## END SECRET CONFIGURATION


INSTALLED_APPS += (

)


# overload media urls for deploy multiple sites
#config.readfp(open(CONFIG_FILE))
#url_root = config.get('current', 'url_root')

#STATIC_URL = project_name + '/static/'
#MEDIA_URL = project_name + '/media/'

#print STATIC_URL
#ADMIN_MEDIA_PREFIX += project_name
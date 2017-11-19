# encoding: utf-8

"""
Django settings for ihmc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9+u!*#lzy1r)6@-1ff2i9nq1b4k59+5a$&lc!a9^6+nn)@4p@('

# SECURITY WARNING: don't run with debug turned on in production!
DEV = False

DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', 'ussamkongre.com','www.ussamkongre.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'bootstrapform',
    'common',
    # 'django.contrib.sites',
    'registration',
    'pages',
    'seo',
    'payments',
    'easy_thumbnails',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'pages.context_processors.site',
)

ROOT_URLCONF = 'hhac.urls'

WSGI_APPLICATION = 'hhac.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'tr'

ugettext = lambda s: s # dummy ugettext function, as django's docs say

LANGUAGES = (
    ('tr', u'Türkçe'),
    ('en', u'English'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = False

SITE_ID = 1

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)


SERVER_EMAIL = ""
DEFAULT_FROM_EMAIL = ""
EMAIL_HOST = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = 25
EMAIL_USE_TLS = True

ACCOUNT_ACTIVATION_DAYS = 7

AUTH_USER_MODEL = 'registration.User'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

SEO_FOR_MODELS = (
    'django.contrib.sites.models.Site',
)

THUMBNAIL_ALIASES = {
    '': {
        'big': {'size': (800, 0), },
        'normal': {'size': (600, 0),},
        'small': {'size': (200, 200),'autocrop': True, 'crop': 'smart', 'upscale': True,},
        'billboard': {'size': (710, 250),'autocrop': True, 'crop': 'smart', 'upscale': True,},
    },
}

THUMBNAIL_SUBDIR = 'thumbnails'

'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs','myapp.log'),
        },
    },
    'loggers': {
        # Again, default Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Your own app - this assumes all your logger names start with "myapp."
        'myapp': {
            'handlers': ['logfile'],
            'level': 'WARNING', # Or maybe INFO or DEBUG
            'propagate': False
        },
    },
}
'''
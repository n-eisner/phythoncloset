# -*- coding: utf-8 -*-

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), '..')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, '..', 'db.sqlite3'),  # Or path to database file if using sqlite3.
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    },
}

DATA_DIRECTORY = os.path.join(PROJECT_ROOT, '..', 'data')

# Output emails to STDOUT
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

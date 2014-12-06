import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'db.sqlite3'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

EMAIL_SUBJECT_PREFIX = '[][Stage] '
LOG_ROOT = os.path.join(os.path.dirname(__file__), '../../../logs/stage')

DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'data')

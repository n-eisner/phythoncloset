# -*- coding: utf-8 -*-

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), '..')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, '..', '..', 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

DATA_DIRECTORY = os.path.join(PROJECT_ROOT, '..', '..', 'data')

COMPRESS_ENABLED = True

EMAIL_SUBJECT_PREFIX = '[Uncloseted][Prod] '
LOG_ROOT = os.path.join(PROJECT_ROOT, '..', '..', 'logs')


TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
	    'django.template.loaders.filesystem.Loader',
	    'django.template.loaders.app_directories.Loader',
	)),
)

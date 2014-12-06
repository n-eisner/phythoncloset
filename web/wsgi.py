import os
import sys
import site

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['DJANGO_CONF'] = 'conf.prod'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
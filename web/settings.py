import os

# Import default settings for the project
from conf.default import *

# We use an environmental variable to indicate the, erm, environment
# This block writes all settings to the local namespace
module_path = os.environ.get('DJANGO_CONF', 'conf.local')
try:
    module = __import__(module_path, globals(), locals(), ['*'])
except ImportError:
    import sys
    print "You need to create a file conf/local.py to contain your local settings"
    sys.exit(1)

for k in dir(module):
    if not k.startswith("__"):
        locals()[k] = getattr(module, k)

# Add any additional apps only required locally
if 'EXTRA_APPS' in locals():
    INSTALLED_APPS = INSTALLED_APPS + EXTRA_APPS

# Adjust settings based on the DISABLED_APPS setting
if 'DISABLED_APPS' in locals():
    INSTALLED_APPS = [k for k in INSTALLED_APPS if k not in DISABLED_APPS]
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    for a in DISABLED_APPS:
        for x, m in enumerate(MIDDLEWARE_CLASSES):
            if m.startswith(a):
                MIDDLEWARE_CLASSES.pop(x)
    TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS)
    for x, m in enumerate(TEMPLATE_CONTEXT_PROCESSORS):
        if m.startswith(a):
            TEMPLATE_CONTEXT_PROCESSORS.pop(x)
    DATABASE_ROUTERS = list(DATABASE_ROUTERS)
    for x, m in enumerate(DATABASE_ROUTERS):
        if m.startswith(a):
            DATABASE_ROUTERS.pop(x)

# Keep version number here - this is generally overwritten as
# part of deployment to be the build name
VERSION = 'UNVERSIONED'

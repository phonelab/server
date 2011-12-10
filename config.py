## IMPORTANT CONFIGS

import os
import django

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DATABASE_ENGINE = 'django.db.backends.sqlite3'
DATABASE_NAME = os.path.join(SITE_ROOT) + '/server.sqlite3'


print DJANGO_ROOT
print SITE_ROOT
print DATABASE_NAME
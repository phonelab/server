# Django settings for server project.

import os
import django

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
## Note: These variables are overridden
## below if production and staging
# Log Path
RAW_LOG_ROOT = os.path.join(SITE_ROOT, 'datalogger', 'logs')
# Application Path
RAW_APP_ROOT = os.path.join(SITE_ROOT, 'application', 'apps')
#IRB Letter path
RAW_IRB_ROOT = os.path.join(SITE_ROOT, 'experiment', 'IRBletters')
#Participant agreement path
RAW_AGREEMENT_ROOT = os.path.join(SITE_ROOT, 'users', 'Participant_Agreement')
#Lookup File path
RAW_LOOKUP_ROOT = os.path.join(SITE_ROOT, 'users', 'Lookup_File')
# Env variable
ENV = os.environ.get("ENV") or "development"

#django_cron 
CRON_POLLING_FREQUENCY = 60

# GEmail setting
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'phonelab.activation'
#EMAIL_HOST_PASSWORD = 'phonelab2012'
#EMAIL_PORT = 587
#FROM_EMAIL = EMAIL_HOST_USER

# Amazon ses Email setting
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAIDSLZDH6UL3PJJMQ'
EMAIL_HOST_PASSWORD = 'Avkt1coRYp2ZPClhP2oVNtO91sjqM3JaStMu5fB7AU6d'
EMAIL_PORT = 465
FROM_EMAIL = 'PhoneLab Team <ops@phone-lab.org>'
#FROM_EMAIL = 'PhoneLab Team <join@phone-lab.org>'

#Movile setting
MOBILE_UTILS_SETTINGS = {
    'MOBILE_TEMPLATES_DIR': (              # tuple of mobile template dirs (absolute paths
    (os.path.join(SITE_ROOT, 'templates/mobile')),
    ),
    'IGNORE_LIST':(                        #tuple of browsers to ignore
        'ipad',
        'palm',
        'wap',
    ),
    'USER_AGENTS_FILE' : (os.path.join(SITE_ROOT, 'mobile_utils/' 'data/' 'mobile_agents.txt')),  # line-broken strings to match
    'USE_REGEX':False                      # use RegEx to do the string search
}

ADMINS = (
#    ('Micheal Benedict', 'micheala@buffalo.edu'),
    ('Taeyeon Ki', 'tki@buffalo.edu'),
)

# C2DM Auth Token
C2DM_AUTH_TOKEN = "DQAAAMgAAAAnzB8fGC_zo5zbiDFzx9mAl55V5SMCrqmWYAPCdcUgNwrTlFHaON81KFPXzGfvbgYNVGuxseJec_QsKPrHYzg0AsoeqrHDNOy2GbUsZcSjVF71SvxU__MIosf0K2Ih04Xhl4hpvxYqSXfvhGfcPe5Vx4MkyaEnOjXy82vhQs93JymjOtvzyi0dA6MRxJUctwk7LdrGZFs7kr6FsVTjJ3XmDtG3GbpKgWjREHotYs3u1p7tBfRjj67EPsdzIv-v1DabPyo4T0oeD2f4uv54ONay"

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#Deprecated in Django 1.4: This setting has been obsoleted by the django.contrib.staticfiles app integration.
#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    (os.path.join(SITE_ROOT, 'static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
		'django.contrib.staticfiles.finders.FileSystemFinder',
		'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-(8mq(psp19h310((%z8(s%4^t1rv((7m+tmae6n--sum86#w)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#Mobile template
    'mobile_utils.loaders.load_template_source',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#Mobile Middleware
    'mobile_utils.middleware.RequestMiddleware',
)

ROOT_URLCONF = 'server.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
    os.path.join(SITE_ROOT, 'templates/admin'),
#    os.path.join(SITE_ROOT, 'templates/mobile'),
)

INSTALLED_APPS = (
		'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Activating the administration interface (needs .auth, .contenttypes, sessions, messages)
    'django.contrib.admin', 
    'application', # application
    'manifest', # manifest
    'datalogger', # datalogger
    'device', # device
    'error', # error
    'transaction', # transaction
    'users', #users
    'experiment', #experiment
    'admin', #admin
    'south', #south
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
# Session and the settings for User processes;
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
AUTH_PROFILE_MODULE = 'users.UserProfile'
# database vars
# production vars
if ENV == "production":
    # TODO
    # need to move all this stuff to S3
    
    # Log Path
    RAW_LOG_ROOT = os.path.join("/mnt", 'datalogger', 'logs')
    # Log Path
    RAW_APP_ROOT = os.path.join("/mnt", 'apps')
    # Add gunicorn
    INSTALLED_APPS += ("gunicorn",)
    from config_production import *

elif ENV == "staging":
    # Log Path
    RAW_LOG_ROOT = os.path.join("/mnt", 'datalogger', 'logs')
    # Log Path
    RAW_APP_ROOT = os.path.join("/mnt", 'apps')
    # Add gunicorn
    INSTALLED_APPS += ("gunicorn",)
    from config_staging import *
else:
    from config_development import *

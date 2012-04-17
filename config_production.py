DATABASE_ENGINE = 'django.db.backends.mysql'
DATABASE_NAME = "phonelab"

DATABASES = {
    'default': {
        'ENGINE'    : DATABASE_ENGINE, # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME'      : DATABASE_NAME,   # Or path to database file if using sqlite3.
        'USER'      : 'phonelab', # Not used with sqlite3.
        'PASSWORD'  : 'dbs3rv3r', # Not used with sqlite3.
        'HOST'      : 'phonelab-backend-db.cg2akhwze6m8.us-east-1.rds.amazonaws.com', # Set to empty string for localhost. Not used with sqlite3.
        'PORT'      : '', # Set to empty string for default. Not used with sqlite3.
    }
}

DEBUG = False
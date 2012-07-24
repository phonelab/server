#!/bin/bash
# This is the shell script for south to migrate DB.
# Separate Projects would need a copy of this script 
# with appropriate Settings export statments.
export DJANGO_SETTINGS_MODULE=settings

python manage.py convert_to_south app.application
python manage.py convert_to_south app.device
python manage.py convert_to_south app.experiment
python manage.py convert_to_south app.transaction
python manage.py convert_to_south app.users

python manage.py schemamigration app.application --auto
python manage.py schemamigration app.device --auto
python manage.py schemamigration app.experiment --auto
python manage.py schemamigration app.transaction --auto
python manage.py schemamigration app.users --auto


python manage.py migrate app.application
python manage.py migrate app.device
python manage.py migrate app.experiment
python manage.py migrate app.transaction
python manage.py migrate app.users

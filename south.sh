#!/bin/bash
# This is a shell script to run south to migrate DB.

PYTHONPATH="${PYTHONPATH}:/home/ec2-user"
export PYTHONPATH
#export ENV=staging
export DJANGO_SETTINGS_MODULE=server.settings
if [ "$1" == "convert" ]
then
  python manage.py convert_to_south app.application
  python manage.py convert_to_south app.device
  python manage.py convert_to_south app.experiment
  python manage.py convert_to_south app.transaction
  python manage.py convert_to_south app.users
  mv /home/ec2-user/server/application/migrations/ /home/ec2-user/south/application/
  mv /home/ec2-user/server/device/migrations/ /home/ec2-user/south/device/
  mv /home/ec2-user/server/experiment/migrations/ /home/ec2-user/south/experiment/
  mv /home/ec2-user/server/transaction/migrations/ /home/ec2-user/south/transaction/
  mv /home/ec2-user/server/users/migrations/ /home/ec2-user/south/users/
elif [ "$1" == "schemamigration" ]
then
  mv /home/ec2-user/south/application/migrations/ /home/ec2-user/server/application/
  mv /home/ec2-user/south/device/migrations/ /home/ec2-user/server/device/
  mv /home/ec2-user/south/experiment/migrations/ /home/ec2-user/server/experiment/
  mv /home/ec2-user/south/transaction/migrations/ /home/ec2-user/server/transaction/
  mv /home/ec2-user/south/users/migrations/ /home/ec2-user/server/users/
  python manage.py schemamigration app.application --auto
  python manage.py schemamigration app.device --auto
  python manage.py schemamigration app.experiment --auto
  python manage.py schemamigration app.transaction --auto
  python manage.py schemamigration app.users --auto
  mkdir test
elif [ "$1" == "migrate" ]
then
  python manage.py migrate app.application
  python manage.py migrate app.device
  python manage.py migrate app.experiment
  python manage.py migrate app.transaction
  python manage.py migrate app.users
else
  echo "\
  Usage: $0 [OPTION]
  Django database migrations with South
  Example: $0 convert
OPTION:
  convert,  convert to a South-managed application
  schemamigration, get South to create an automatic migration
  migrate, apply your newly created migration to your database"
fi

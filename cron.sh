#!/bin/bash
# This is a Django, Project-specific Cron script.
# Separate Projects would need a copy of this script 
# with appropriate Settings export statments.

PYTHONPATH="${PYTHONPATH}:/home/ec2-user"
export PYTHONPATH
export DJANGO_SETTINGS_MODULE=server.settings

python /home/ec2-user/server/cron.py

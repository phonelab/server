#!/bin/bash
# This is a Django, Project-specific Cron script.
# Separate Projects would need a copy of this script 
# with appropriate Settings export statments.

export DJANGO_SETTINGS_MODULE=settings

python /home/tki/Workspace/PhoneLab/Github/server/cron.py

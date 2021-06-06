#!/bin/bash

rm -r /home/pyuser/app_data/public/*
python /home/pyuser/app/app/manage.py collectstatic --clear --noinput

echo "DONE."
#!/usr/bin/env bash

# collect static on release
python manage.py collectstatic --noinput -i admin -i django_extensions -i debug_toolbar

# run migrate on release
python manage.py migrate

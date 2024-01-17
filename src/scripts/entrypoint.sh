#!/bin/bash

set -e


# python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80

# uwsgi --socket :80 --master --enable-threads  --plugin=python38 --module core.wsgi

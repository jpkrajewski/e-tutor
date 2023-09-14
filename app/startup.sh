#!/bin/bash
python manage.py wait_for_db 
python manage.py collectstatic --noinput 
python manage.py makemigrations 
python manage.py migrate 
python manage.py runserver 0.0.0.0:$DJANGO_PORT
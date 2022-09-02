release: python manage.py migrate
web: daphne -b 0.0.0.0 -p $PORT etutor.asgi:application
celerybeat: celery -A etutor beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler & celery -A etutor.celery worker -l info & wait -n
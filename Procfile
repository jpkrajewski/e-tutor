release: python manage.py migrate
web: daphne -b 0.0.0.0 -p $PORT etutor.asgi:application
celery: celery -A etutor.celery worker --pool=solo -l info
celerybeat: celery -A etutor beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
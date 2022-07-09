import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etutor.settings')

app = Celery('etutor')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'check-incoming-lessons-every-10-minutes': {
        'task': 'app.tasks.check_incoming_lessons',
        'schedule': crontab(),
    },

    'update-lessons-date-at-1am': {
        'task': 'app.tasks.update_lessons_dates',
        'schedule': crontab(),
        # 'args': ()
    },


}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

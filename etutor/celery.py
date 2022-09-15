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
    'send-lesson-reminders-every-15-minutes': {
        'task': 'app.tasks.send_lesson_reminders',
        'schedule': crontab(minute='*/10'),
    },

    'organize-done-lessons-at-Sunday-11:59': {
        'task': 'app.tasks.organize_done_lessons',
        'schedule': crontab(day_of_week='sunday', hour=23, minute=30),
    },

    'send-best-message': {
        'task': 'app.tasks.send_alpha_message',
        'schedule': crontab(hour=11, minute=0),
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

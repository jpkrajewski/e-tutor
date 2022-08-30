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
    'send-lesson-reminder-every-30-seconds': {
        'task': 'app.tasks.send_lesson_reminder',
        'schedule': crontab(),
    },

    'organize-done_lessons-date-at-1am': {
        'task': 'app.tasks.organize_done_lessons',
        'schedule': crontab(),
        # 'args': ()
    },

    'create-lesson-room-every-30-seconds': {
        'task': 'app.tasks.create_lesson_room',
        'schedule': crontab(),
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

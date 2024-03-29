import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etutor.settings")

app = Celery("etutor")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "check-ready-lessons-create-lesson-rooms-send-reminders-create-payments-every-5min": {
        "task": "app.tasks.check_ready_lessons_create_lesson_rooms_send_reminders_create_payments",
        "schedule": crontab(minute="*/5"),
    },
    "organize-done-lessons-at-Sunday-23:59": {
        "task": "app.tasks.organize_done_lessons",
        "schedule": crontab(day_of_week="sunday", hour=23, minute=30),
    },
    "delete-inactive-teaching-rooms-at-23:59-every-day": {
        "task": "app.tasks.delete_inactive_teaching_rooms",
        "schedule": crontab(hour=23, minute=30),
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.timezone = "UTC"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

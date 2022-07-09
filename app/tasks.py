from celery import shared_task
from .utils import LessonsUpdater, NotificationHandler, FacebookMessengerAPI


@shared_task(bind=True)
def check_incoming_lessons(self):
    notification_handler = NotificationHandler(3, 1)
    if not notification_handler.is_time_to_send_notification():
        return 'No notification to send'

    notification_array = notification_handler.prepare_notification()
    for notification in notification_array:
        FacebookMessengerAPI.call_send(**notification)
    return 'Notifications send'


@shared_task(bind=True)
def update_lessons_dates(self):
    return LessonsUpdater.update()

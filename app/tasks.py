from celery import shared_task
from secrets import token_urlsafe

from .utils import FacebookMessengerAPI, Reminder, ReminderFacebookWrapper
from .models import Lesson, TeachingRoom, Payment, Tutor
from datetime import timedelta, datetime


@shared_task(bind=True)
def send_lesson_reminders(self):

    lessons = Lesson.objects.get_lessons_for_reminders()

    if not lessons:
        return 'No reminders to send'

    facebook_reminders = []
    # mail_reminders = []
    # sms_reminders = []

    for lesson in lessons:
        if lesson.place == Lesson.ONLINE:
            TeachingRoom(lesson=lesson, url=token_urlsafe(16)).save()

        reminder = Reminder(lesson.tutor.message_template_to_tutor, lesson).get_reminder_content()

        # facebook sending
        if lesson.send_facebook_message:
            facebook_reminders.append(ReminderFacebookWrapper(lesson.tutor.int_facebook_psid, reminder).get_reminder())

        # sms sending
        ...
        # mail sending
        ...

        # create missing payment record to track cash flow
        lp = Payment(student=lesson.student, lesson_date=lesson.start_datetime, amount=lesson.amount)
        lp.save()

        lesson.is_notification_send = True
        lesson.save()

    for facebook_reminder in facebook_reminders:
        FacebookMessengerAPI.call_send(facebook_reminder)

    # for mail_reminder in mail_reminders:
    ...
    # for sms_reminder in sms_reminders:
    ...

    return 'Reminders send'


@shared_task(bind=True)
def organize_done_lessons(self):
    done_lessons = Lesson.objects.get_done_lessons()

    if not done_lessons:
        return 'No lessons were updated'

    for lesson in done_lessons:
        lesson.is_notification_send = False
        lesson.start_datetime += timedelta(days=7)
        lesson.end_datetime += timedelta(days=7)
        lesson.save()

        if lesson.place == Lesson.ONLINE:
            lesson.teachingroom.delete()

    return 'Organized successfully'


@shared_task(bind=True)
def send_alpha_message(self):
    """
    You are the best.
    """
    FacebookMessengerAPI.call_send(ReminderFacebookWrapper(psid=Tutor.objects.get(1).int_facebook_psid, message='Jesteś najlepszy').get_reminder())
    return 'Jesteś najlepszy'

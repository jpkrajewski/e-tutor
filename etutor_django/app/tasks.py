from celery import shared_task
from secrets import token_urlsafe

from app.utils import Reminder
from app.models import Lesson, TeachingRoom, Payment, Tutor
from datetime import timedelta


@shared_task(bind=True)
def check_ready_lessons_create_lesson_rooms_send_reminders_create_payments(self):
    lessons = Lesson.objects.get_lessons_for_reminders()
    if not lessons:
        return "No reminders to send"
    facebook_reminders = []
    # mail_reminders = []
    # sms_reminders = []
    for lesson in lessons:
        if lesson.place == Lesson.ONLINE:
            TeachingRoom(lesson=lesson, url=token_urlsafe(16)).save()
        reminder = Reminder(
            lesson.tutor.message_template_to_tutor, lesson
        ).get_content()
        # facebook sending

        # sms sending
        ...
        # mail sending
        ...
        # create missing payment record to track cash flow
        lp = Payment(
            student=lesson.student,
            lesson_date=lesson.start_datetime,
            amount=lesson.amount,
        )
        lp.save()
        lesson.is_notification_send = True
        lesson.save()
    # for mail_reminder in mail_reminders:
    ...
    # for sms_reminder in sms_reminders:
    ...
    return "Reminders send"


@shared_task(bind=True)
def set_repetitive_lessons_to_next_week(self):
    """
    Organize done lessons:

    1. Delete non repetitive lessons
    3. Update repetitive lessons for next week


    Too much for 1 function and teaching rooms stay for a week in a bad curcomstances
    """
    done_lessons = Lesson.objects.get_done_lessons()
    if not done_lessons:
        return "No lessons were updated"

    log = []
    for lesson in done_lessons:
        if lesson.is_repetitive is False:
            log.append(f"Lesson with id: {lesson.id} has been deleted.")
            lesson.delete()
            continue

        lesson.is_notification_send = False
        lesson.start_datetime += timedelta(days=7)
        lesson.end_datetime += timedelta(days=7)
        lesson.save()
        log.append(f"Lesson with id: {lesson.id} has been updated.")

    return "\n".join(log)


@shared_task(bind=True)
def delete_inactive_teaching_rooms(self):
    teaching_rooms = TeachingRoom.objects.get_inactive()

    if not teaching_rooms:
        return "No teaching rooms to delete"

    for room in teaching_rooms:
        room.delete()

    return "Inactive rooms deleted"

from celery import shared_task
from secrets import token_urlsafe
import boto3
from datetime import timedelta

from django.conf import settings

from app.utils import TemplatePopulator, SesMailSender
from app.models import Lesson, TeachingRoom, Payment



@shared_task(bind=True)
def check_ready_lessons_create_lesson_rooms_send_reminders_create_payments(self):
    lessons = Lesson.objects.get_lessons_for_reminders()
    if not lessons:
        return "No reminders to send"
    mail_sender = SesMailSender(
        boto3.client(
            service_name='ses', 
            region_name=settings.AWS_SES_REGION_NAME,
            aws_access_key_id=settings.AWS_SES_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SES_SECRET_ACCESS_KEY
        )
    )
    for lesson in lessons:
        if lesson.place == Lesson.ONLINE:
            TeachingRoom(lesson=lesson, url=token_urlsafe(16)).save()
        if lesson.send_email:
            populator = TemplatePopulator(lesson)
            email_html, email_text = populator.get_email_to_tutor()
            mail_sender.send_email(
                source=settings.AWS_SES_SOURCE_EMAIL,
                destination=lesson.tutor.user.email,
                subject="ETutor - Lesson reminder",
                text=email_text,
                html=email_html,
            )
            # email_html, email_text = populator.get_email_to_student()
            # mail_sender.send_email(
            #     source=AWS_SES_SOURCE_EMAIL,
            #     destination=lesson.student.user.email,
            #     subject="ETutor - Lesson reminder",
            #     text=email_text,
            #     html=email_html,
            # )
        if lesson.send_sms:
            pass
        lp = Payment(
            student=lesson.student,
            lesson_date=lesson.start_datetime,
            amount=lesson.amount,
        )
        lp.save()
        lesson.is_notification_send = True
        lesson.save()
    return "Reminders send"


@shared_task(bind=True)
def set_repetitive_lessons_to_next_week(self):
    done_lessons = Lesson.objects.get_done_lessons()
    if not done_lessons:
        return "No lessons were updated"
    for lesson in done_lessons:
        if not lesson.is_repetitive:
            lesson.delete()
        lesson.is_notification_send = False
        lesson.start_datetime += timedelta(days=7)
        lesson.end_datetime += timedelta(days=7)
        lesson.save()
    return "Lessons updated"


@shared_task(bind=True)
def delete_inactive_teaching_rooms(self):
    teaching_rooms = TeachingRoom.objects.get_inactive()
    if not teaching_rooms:
        return "No teaching rooms to delete"
    for room in teaching_rooms:
        room.delete()
    return "Inactive rooms deleted"

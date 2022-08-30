from celery import shared_task
from .utils import FacebookMessengerAPI, FacebookReminder
from .models import Tutor, Lesson, TeachingRoom
from django.utils import timezone
from datetime import timedelta, datetime
from secrets import token_urlsafe


@shared_task(bind=True)
def send_lesson_reminder(self):
    tutors = Tutor.objects.filter(account_active__lte=datetime.now(tz=timezone.utc),
                                  send_reminders_to_yourself=True)

    if not tutors:
        return 'No reminders send, because there are no tutors'

    facebook_reminders = []
    for tutor in tutors:
        lessons = tutor.lesson_set.get_lessons_for_reminders(hours_before=tutor.send_reminder_hours_before,
                                                             datetime_now=datetime.now(tz=timezone.utc))
        for lesson in lessons:
            facebook_reminders.append(FacebookReminder(psid=tutor.psid,
                                                       template=tutor.message_template_to_yourself,
                                                       lesson=lesson).get_reminder())
            lesson.facebook_notification_send = True
            lesson.save()

    if not facebook_reminders:
        return 'No notification to send'

    response = []
    for reminder in facebook_reminders:
        response.append(FacebookMessengerAPI.call_send(reminder))
        response.append(reminder)
    return response


@shared_task(bind=True)
def create_lesson_room(self):
    lessons = Lesson.objects.get_lessons_ready_for_creating_teaching_room(datetime_now=datetime.now(tz=timezone.utc))
    if not lessons:
        return 'No teaching rooms were created'

    response = []
    for lesson in lessons:
        teaching_room = TeachingRoom(url=token_urlsafe(50), lesson=lesson)
        teaching_room.save()
        response.append(str(teaching_room))

    return 'Rooms created: ' + str(response)


@shared_task(bind=True)
def organize_done_lessons(self):
    done_lessons = Lesson.objects.get_done_lessons()

    if not done_lessons:
        return 'No lessons were updated'

    response = []
    for lesson in done_lessons:
        lesson_flow_info = []
        try:
            # delete teaching room
            lesson.teachingroom.delete()
            lesson_flow_info = f'{str(lesson)} teaching room deleted'
        except lesson.teachingroom.RelatedObjectDoesNotExist as e:
            lesson_flow_info = f'{str(lesson)} teaching room not deleted: {e}'

        if lesson.repetitive:
            # update lesson to be next week
            lesson.start_datetime += timedelta(days=7)
            lesson.end_datetime += timedelta(days=7)
            lesson.save()
            lesson_flow_info += 'Updated successfully'

        response.append(' '.join(lesson_flow_info))
    return str(response)

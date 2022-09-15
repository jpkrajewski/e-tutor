from datetime import datetime, timedelta, tzinfo

from django.utils import timezone
from django.test import TestCase, SimpleTestCase
from django.conf import settings
from django.contrib.auth.models import User

from .models import Tutor, Student, Lesson
from .tasks import organize_done_lessons
from .utils import FacebookMessengerAPI, ReminderFacebookWrapper, Reminder


class DebugTest(SimpleTestCase):
    def test_debug_mode(self):
        """
        Debug must be set to False
        """

        self.assertEqual(settings.DEBUG, False)


class TasksLessonsTest(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(username='testuser', password='12345')
        self.tutor = Tutor.objects.create(user=user)
        self.student = Student.objects.create(
            first_name='Jan', last_name='Kowalski', tutor=self.tutor)
        return super().setUp()


    def test_deleting_of_non_repetitive_lessons(self):
        """
        If lesson is done and is not repetitive it must be deleted
        """
        yesterday = datetime.now(tz=timezone.utc) - timedelta(days=1)
        Lesson.objects.create(subject='Math', 
                                place=Lesson.AT_TUTORS, 
                                amount=100, 
                                is_repetitive=False, 
                                start_datetime=yesterday, 
                                end_datetime=yesterday, 
                                tutor=self.tutor, 
                                student=self.student
                            )
        
        log = organize_done_lessons()
        self.assertQuerysetEqual(Lesson.objects.all(), Lesson.objects.none())
        self.assertEqual(log, 'Lesson with id: 1 has been deleted.')

    def test_setting_done_lesson_to_next_week(self):
        """
        If lesson is done and is repetitive it must be set to next week (+7days)
        """

        yesterday = datetime.now(tz=timezone.utc) - timedelta(days=1)
        lesson = Lesson.objects.create(subject='Math', 
                                place=Lesson.AT_TUTORS, 
                                amount=100, 
                                is_repetitive=True, 
                                start_datetime=yesterday, 
                                end_datetime=yesterday, 
                                tutor=self.tutor, 
                                student=self.student
                            )
        
        log = organize_done_lessons()
        self.assertEqual(Lesson.objects.filter(start_datetime=yesterday + timedelta(days=7)).first(), lesson)
        self.assertEqual(log, 'Lesson with id: 1 has been updated.')


    def test_sending_reminders(self):
        """
        Test sending message to fb
        """

        now = datetime.now(tz=timezone.utc)
        lesson = Lesson.objects.create(subject='Math', 
                            place=Lesson.AT_TUTORS, 
                            amount=100, 
                            is_repetitive=True, 
                            start_datetime=now, 
                            end_datetime=now, 
                            tutor=self.tutor, 
                            student=self.student
                        )


        content = Reminder('Works', lesson).get_content()
        fb_wrapper = ReminderFacebookWrapper(self.tutor.facebook_psid, content)
        response = FacebookMessengerAPI.call_send(fb_wrapper.get_message())
        self.assertEqual(response['recipient_id'], self.tutor.facebook_psid, 
            msg=f'Response recipient id should be: {self.tutor.facebook_psid}, instead got response {response}')

    

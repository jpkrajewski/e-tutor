from datetime import datetime, timedelta
import boto3

from django.utils import timezone
from django.test import TestCase, SimpleTestCase
from django.conf import settings
from django.contrib.auth.models import User

from app.models import Tutor, Student, Lesson
from app.tasks import set_repetitive_lessons_to_next_week
from app.utils import TemplatePopulator, SesMailSender


class TestSesMailSender(TestCase):
    def setUp(self):
        self.mail_sender = SesMailSender(
            boto3.client(
                service_name="ses",
                region_name=settings.AWS_SES_REGION_NAME,
                aws_access_key_id=settings.AWS_SES_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SES_SECRET_ACCESS_KEY,
            )
        )

    def test_send_email(self):
        message_id = self.mail_sender.send_email(
            source=settings.AWS_SES_SOURCE_EMAIL,
            destination=settings.AWS_SES_SOURCE_EMAIL,
            subject="Test",
            text="Test",
            html="<h1>Test</h1>",
        )
        self.assertIsNotNone(message_id)


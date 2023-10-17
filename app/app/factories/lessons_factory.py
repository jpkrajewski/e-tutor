from datetime import datetime, timezone

import factory

from app.factories.students_factory import StudentFactory
from app.factories.tutor_factory import TutorFactory
from app.models import Lesson


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson

    subject = factory.Faker("word")
    place = factory.Faker("random_element", elements=["Online", "Client's", "Tutor's"])
    amount = factory.Faker("random_int")
    description = factory.Faker("text")
    start_datetime = datetime(2023, 10, 17, tzinfo=timezone.utc)
    end_datetime = datetime(2023, 10, 17, tzinfo=timezone.utc)
    is_repetitive = True
    is_notification_send = True
    send_email = False
    send_sms = False
    tutor = factory.SubFactory(TutorFactory)
    student = factory.SubFactory(StudentFactory)

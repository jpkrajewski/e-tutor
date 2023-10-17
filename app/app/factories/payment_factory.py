from datetime import datetime, timezone

import factory

from app.factories.students_factory import StudentFactory
from app.models import Payment


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    lesson_date = datetime(2023, 10, 17, tzinfo=timezone.utc)
    amount = factory.Faker("random_int")
    status = factory.Faker("random_element", elements=["paid", "due"])
    student = factory.SubFactory(StudentFactory)

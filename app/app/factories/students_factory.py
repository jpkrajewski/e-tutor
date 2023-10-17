import factory

from app.factories.tutor_factory import TutorFactory
from app.models import Student


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    address = factory.Faker("address")
    education_level = factory.Faker("job")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    discord_nick = factory.Faker("user_name")
    facebook_profile = factory.Faker("url")
    tutor = factory.SubFactory(TutorFactory)

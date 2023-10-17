import factory

from app.factories.user_factory import UserFactory
from app.models import Tutor


class TutorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tutor

    user = factory.SubFactory(UserFactory)

import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """User model factory"""

    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.django.Password("pw")
    is_staff = False
    is_superuser = False
    is_active = True

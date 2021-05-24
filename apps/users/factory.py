import factory
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    @factory.lazy_attribute
    def first_name(self):
        fake = Faker(locale='en-US')
        return fake.first_name()

    @factory.lazy_attribute
    def last_name(self):
        fake = Faker(locale='en-US')
        return fake.last_name()

    @factory.lazy_attribute
    def email(self):
        return slugify(self.username) + '@fake.fake'

    username = factory.Sequence(lambda n: f'fake_user_{n}')

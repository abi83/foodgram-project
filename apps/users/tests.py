from uuid import uuid1

from faker import Faker
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


from apps.users.factory import UserFactory

User = get_user_model()


class UserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fake = Faker()
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        pass

    def test_new_user_registration(self):
        """
        POST request on 'signup' page creates new user
        """
        new_user = UserFactory.create()
        passwd = str(uuid1())
        post_data = {
            'first_name': new_user.first_name,
            'last_name': new_user.last_name + 'jj',
            'email': new_user.email,
            'username': new_user.username,
            'password1': passwd,
            'password2': passwd,
        }
        self.client.post(
            reverse('signup'),
            post_data,
            follow=True)
        user_from_db = User.objects.get(username=new_user.username)
        for field in post_data:
            if not field.startswith('password'):
                with self.subTest(msg=f'Checking {field} field'):
                    self.assertEqual(
                        getattr(user_from_db, field),
                        post_data[field],
                        f'User creation form returns wrong {field} field'
                    )

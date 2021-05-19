from uuid import uuid1

from faker import Faker
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


from apps.users.factory import UserFactory
from apps.users.forms import CreationForm

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
            'last_name': new_user.last_name,
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
        with self.subTest(msg='Checking if login is possible'):
            self.client.force_login(user_from_db)
            self.assertEqual(
                int(self.client.session['_auth_user_id']),
                user_from_db.pk,
                'Created user can not login'
            )

    def test_email_field_is_required(self):
        new_user = UserFactory.create()
        passwd = str(uuid1())
        user_data = {
            'username': new_user.username,
            'password1': passwd,
            'password2': passwd,
        }
        form = CreationForm(data=user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_already_exist(self):
        new_user = UserFactory.create()
        new_user.save()
        passwd = str(uuid1())
        user_data = {
            'username': new_user.username,
            'email': new_user.email,
            'password1': passwd,
            'password2': passwd,
        }
        form = CreationForm(data=user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


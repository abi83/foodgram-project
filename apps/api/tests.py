from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from faker import Faker

from apps.recipes.models import Unit, Ingredient

User = get_user_model()


class ApiTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fake = Faker()
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        pass

    def test_ingredients_filter(self):
        """
        Very basic test example
        """
        unit = Unit.objects.create(name='test-unit', short='t-un')
        unit.save()
        names = ['one', 'two', 'one two']
        ingredients = [Ingredient(name=name, unit=unit) for name in names]
        Ingredient.objects.bulk_create(ingredients)
        for query in names:
            with self.subTest(msg=f'Checking {query} query'):
                resp = self.client.get(
                    reverse('api:ingredient-api') + f'?query={query}')
                self.assertEqual(resp.status_code, 200)

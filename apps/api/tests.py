from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from apps.recipes.models import Ingredient, Unit

User = get_user_model()


class ApiTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fake = Faker()
        cls.client = Client()
        cls.unit = Unit.objects.create(name='test-unit', short='t-un')
        cls.unit.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_ingredients_filter(self):
        """
        Very basic test example
        """
        names = ['one', 'two', 'one two']
        ingredients = [Ingredient(name=name, unit=self.unit) for name in names]
        Ingredient.objects.bulk_create(ingredients)
        for query in names:
            with self.subTest(msg=f'Checking {query} query'):
                resp = self.client.get(
                    reverse('api:ingredient-api') + f'?query={query}')
                self.assertEqual(resp.status_code, 200)

import random
import uuid

import factory
from PIL.ImageColor import colormap
from django.contrib.auth import get_user_model
from factory import django, fuzzy
from faker import Faker

from apps.recipes.models import Recipe, Ingredient, RecipeIngredient
from apps.users.factory import UserFactory

User = get_user_model()


class RecipeFactory(django.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    time = factory.fuzzy.FuzzyInteger(3, 120)

    image = factory.django.ImageField(
        filename=str(uuid.uuid1) + '.jpg',
        width=factory.fuzzy.FuzzyInteger(100, 1500),
        height=factory.fuzzy.FuzzyInteger(100, 1500),
        color=factory.fuzzy.FuzzyChoice(colormap)
    )

    @factory.lazy_attribute
    def title(self):
        fake = Faker(locale='en-US')
        return fake.catch_phrase()

    @factory.lazy_attribute
    def description(self):
        fake = Faker()
        sentences = random.randint(2, 7)
        return ' '.join(fake.paragraphs(nb=sentences))

    @factory.lazy_attribute
    def tag_breakfast(self):
        return Faker().pybool()

    @factory.lazy_attribute
    def tag_lunch(self):
        return Faker().pybool()

    @factory.lazy_attribute
    def tag_dinner(self):
        return Faker().pybool()

    @factory.post_generation
    def ingredients(self, create, extracted):
        if not create:
            return
        if extracted:
            for ingredient in extracted:
                if random.random() < 0.01:
                    self.ingredients.add(ingredient)

    class Meta:
        model = Recipe


class RecipeIngredientFactory(django.DjangoModelFactory):
    recipe = factory.SubFactory(RecipeFactory)
    ingredient = factory.SubFactory(Ingredient)
    count = fuzzy.FuzzyInteger(1, 40)

    class Meta:
        model = RecipeIngredient

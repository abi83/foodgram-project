import random
import uuid

import factory
from django.contrib.auth import get_user_model
from factory import django, fuzzy
from faker import Faker
from PIL.ImageColor import colormap

from apps.recipes.models import Ingredient, Recipe, RecipeIngredient
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

    @factory.post_generation
    def tags(self, create, extracted):
        if not create:
            return
        if extracted:
            for tag in extracted:
                if random.random() < 0.3:
                    self.tags.add(tag)

    class Meta:
        model = Recipe


class RecipeIngredientFactory(django.DjangoModelFactory):
    recipe = factory.SubFactory(RecipeFactory)
    ingredient = factory.SubFactory(Ingredient)
    count = fuzzy.FuzzyInteger(1, 40)

    class Meta:
        model = RecipeIngredient

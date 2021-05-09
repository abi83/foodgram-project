import logging
import os
import factory
import random

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from factory import django, fuzzy


from apps.recipes.models import Ingredient, Recipe
from apps.recipes.factory import RecipeFactory, RecipeIngredientFactory

User = get_user_model()

logger = logging.getLogger('foodgram')


class Command(BaseCommand):
    help = 'Populate Recipes, and fill them with random count of Ingredients.'

    RECIPES = 50

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int, default=self.RECIPES)

    def show_progress(self, progress, instance_name):
        width = 40
        points = int(width * progress)
        backspaces = width - points
        bar = ('[' + '.' * points + ' ' * backspaces + '] '
               + str(int(progress * 100)) + ' %')
        text = f'Populating {instance_name} '.ljust(25)
        self.stdout.write(
            self.style.SUCCESS(text + bar),
            ending='\r'
        )

    def report_success(self, number, instance_name):
        self.stdout.write(' ' * 100, ending='\r')
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {number} {instance_name}'
            ))

    def populate_recipes(self, number):
        for i in range(number):
            self.show_progress(i / number, 'Recipes')
            author = fuzzy.FuzzyChoice(User.objects.all())
            RecipeFactory.create(author=author)
        self.report_success(number, 'Recipes')

    def populate_recipes_with_ingredients(self):
        recipes = Recipe.objects.all()
        i = 0
        for recipe in recipes:
            self.show_progress(i / len(recipes), 'Recipe-Ingredient')
            for n in range(random.randint(2, 10)):
                ingredient = fuzzy.FuzzyChoice(Ingredient.objects.all())
                count = fuzzy.FuzzyInteger(1, 40)
                RecipeIngredientFactory.create(recipe=recipe, ingredient=ingredient, count=count)
            i += 1
        self.report_success(len(recipes), 'Recipe-Ingredient')

    def handle(self, *args, **options):
        number = options['number']
        self.populate_recipes(number)
        self.populate_recipes_with_ingredients()

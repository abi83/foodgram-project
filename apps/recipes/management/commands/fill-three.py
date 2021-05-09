import logging
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from factory import fuzzy

from apps.recipes.factory import RecipeFactory, RecipeIngredientFactory
from apps.recipes.models import Ingredient, Recipe
from foodgram.utils.progress import Progress


User = get_user_model()

logger = logging.getLogger('foodgram')


class Command(BaseCommand):
    help = 'Populate Recipes, and fill them with random count of Ingredients.'

    RECIPES = 50

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int, default=self.RECIPES)

    @staticmethod
    def populate_recipes(number):
        for i in range(number):
            Progress.show_progress(i / number, 'Recipes')
            author = fuzzy.FuzzyChoice(User.objects.all())
            RecipeFactory.create(author=author)
        Progress.report_success(number, 'Recipes')

    @staticmethod
    def populate_recipes_with_ingredients():
        recipes = Recipe.objects.all()
        i = 0
        for recipe in recipes:
            Progress.show_progress(i / len(recipes), 'Recipe-Ingredient')
            for n in range(random.randint(2, 10)):
                ingredient = fuzzy.FuzzyChoice(Ingredient.objects.all())
                count = fuzzy.FuzzyInteger(1, 40)
                RecipeIngredientFactory.create(recipe=recipe, ingredient=ingredient, count=count)
            i += 1
        Progress.report_success(len(recipes), 'Recipe-Ingredient')

    def handle(self, *args, **options):
        number = options['number']
        self.populate_recipes(number)
        self.populate_recipes_with_ingredients()

import csv
import logging
import os

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from apps.recipes.models import Ingredient, Unit
from foodgram.utils.progress import Progress

logger = logging.getLogger('foodgram')


class Command(BaseCommand):
    help = 'Populate initial Ingredients and Units from fixtures data: ' \
           '.apps/recipes/fixtures_data/ingredients.cvs file'

    def handle(self, *args, **options):
        with open(
                os.getcwd() + '\\apps\\recipes'
                              '\\fixtures_data\\ingredients.csv',
                encoding="utf-8") as file:
            lines_count = sum(1 for _ in file)
        with open(
                os.getcwd() + '\\apps\\recipes'
                              '\\fixtures_data\\ingredients.csv',
                encoding="utf-8") as file:
            csv_data = csv.reader(file)
            ingredients = []
            line_number = created_counter = 0
            for line in csv_data:
                # read line
                try:
                    ingredient_name, unit_label = line
                except ValueError as error:
                    logger.warning(error, f'on line: {line}')
                    raise ValueError(
                        f'Fixtures file is invalid in line: {line}') from error
                if unit_label == '':
                    unit_label = '--'
                current_unit = Unit.objects.get_or_create(
                    name=unit_label.lower(),
                    short=unit_label[:9].lower())[0]
                # appending new ingredient
                ingredients.append(
                    Ingredient(
                        name=ingredient_name.lower(),
                        unit=current_unit,
                    )
                )
                # save a set of ingredients
                if len(ingredients) >= 10:
                    try:
                        Ingredient.objects.bulk_create(ingredients)
                        created_counter += 10
                    except IntegrityError:
                        logger.warning(
                            f'Error: some of ingredients in {ingredients}'
                            f'already exists')
                        self.stdout.write(
                            self.style.WARNING(
                                'Some of ingredients already exist'),
                            ending='\r'
                        )
                    ingredients = []
                line_number += 1
                Progress.show_progress(line_number / lines_count,
                                       'Ingredients')
        Progress.report_success(created_counter, 'Ingredients')

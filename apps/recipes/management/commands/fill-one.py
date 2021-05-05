import csv
import logging
import os

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from apps.recipes.models import Unit, Ingredient

logger = logging.getLogger('foodgram')


class Command(BaseCommand):
    help = 'Populate initial Ingredients and Units from fixtures data: ' \
           '.apps/recipes/fixtures_data/ingredients.cvs file'

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

    def handle(self, *args, **options):
        with open(
                os.getcwd() + '\\apps\\recipes\\fixtures_data\\ingredients.csv',
                encoding="utf-8") as file:
            lines_count = sum(1 for _ in file)
        with open(
                os.getcwd() + '\\apps\\recipes\\fixtures_data\\ingredients.csv',
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
                    raise ValueError(f'Fixtures file is invalid in line: {line}') from error
                current_unit = Unit.objects.get_or_create(name=unit_label, short=unit_label[:9])[0]
                # appending new ingredient
                ingredients.append(
                    Ingredient(
                        name=ingredient_name,
                        unit=current_unit,
                    )
                )
                # save a set of ingredients
                if len(ingredients) >= 10:
                    try:
                        Ingredient.objects.bulk_create(ingredients)
                        created_counter += 10
                    except IntegrityError as error:
                        logger.warning(f'Error: some of ingredients in {ingredients} already exists')
                        self.stdout.write(
                            self.style.WARNING('Some of ingredients already exist'),
                            ending='\r'
                        )
                    ingredients = []
                line_number += 1
                self.show_progress(line_number/lines_count, 'Ingredients')
        self.report_success(created_counter, 'Ingredients')

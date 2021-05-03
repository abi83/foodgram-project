import random
import sys
from pathlib import Path
import os
import csv
import logging
logger = logging.getLogger('foodgram')


from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from foods.models import Unit, Ingredient


class Command(BaseCommand):
    help = 'Populate initial Ingredients and Units from fixtures data: ' \
           '.foods/fixtures_data/ingredients.cvs file'

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
                os.getcwd() + '\\foods\\fixtures_data\\ingredients.csv',
                encoding="utf-8") as file:
            lines_count = sum(1 for _ in file)
        with open(
                os.getcwd() + '\\foods\\fixtures_data\\ingredients.csv',
                encoding="utf-8") as file:
            csv_data = csv.reader(file)
            ingredients = []
            units = list(Unit.objects.all())
            units_labels = []
            line_number = 0
            for line in csv_data:
                # read data
                try:
                    ingredient_name, unit_label = line
                except ValueError as error:
                    logger.warning(error, f'on line: {line}')
                    raise ValueError(f'Fixtures file is invalid in line: {line}') from error
                # make a unique set of units and it labels
                if unit_label not in units_labels:
                    units_labels.append(unit_label)
                    try:
                        new_unit = Unit.objects.create(name=unit_label, short=unit_label[:9])
                        units.append(new_unit)
                    except IntegrityError as error:
                        logger.warning(f'Error on unit_label: {unit_label}')
                        self.stdout.write(
                            self.style.WARNING(f'Unit with label "{unit_label}" already exist'),
                            ending='\r'
                        )
                        pass
                # appending new ingredient
                ingredients.append(
                    Ingredient(
                        name=ingredient_name,
                        unit=list(
                            filter(lambda x: x.name == unit_label, units))[0]
                    )
                )
                # save a set of ingredients
                if len(ingredients) > 10:
                    try:
                        Ingredient.objects.bulk_create(ingredients)
                    except IntegrityError as error:
                        logger.warning(f'Error: some of ingredients in {ingredients} already exists')
                        self.stdout.write(
                            self.style.WARNING('Some of ingredients already exist'),
                            ending='\r'
                        )
                        pass
                    ingredients = []
                line_number += 1
                self.show_progress(line_number/lines_count, 'Ingredients')
        self.report_success(line_number, 'Ingredients')

import random
import sys
from pathlib import Path
import os


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
            index = 0
            ingredients = []
            units_labels = []
            for line in file:
                try:
                    ingredient_name, unit_label = line.strip().split(',')
                except ValueError as error:
                    raise ValueError('Fixtures file is invalid') from error
                if unit_label not in units_labels:
                    units_labels.append(unit_label)
                    Unit.objects.create()
                ingredients.append(Ingredient(name=ingredient_name, unit=Unit))
                # ingredients.append(Ingredient())
                # index += 1
                # if index >= 10:
                #     Unit.objects.bulk_create()
                #     Ingredient.objects.bulk_create()
                #     index = 0
                #     ingredients = []
                #     units = []
            print(units_labels)
        self.report_success(100, 'Nothing')

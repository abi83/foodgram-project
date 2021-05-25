import sys
from abc import ABC

from django.core.management.base import BaseCommand, OutputWrapper
from django.core.management.color import color_style


class Progress(BaseCommand, ABC):
    stdout = OutputWrapper(sys.stdout)
    style = color_style()

    @classmethod
    def show_progress(cls, progress, instance_name):
        width = 40
        points = int(width * progress)
        backspaces = width - points
        bar = ('[' + '.' * points + ' ' * backspaces + '] '
               + str(int(progress * 100)) + ' %')
        text = f'Populating {instance_name} '.ljust(25)
        cls.stdout.write(
            cls.style.SUCCESS(text + bar),
            ending='\r'
        )

    @classmethod
    def report_success(cls, number, instance_name):
        cls.stdout.write(' ' * 100, ending='\r')
        cls.stdout.write(
            cls.style.SUCCESS(
                f'Successfully created {number} {instance_name}'
            ))

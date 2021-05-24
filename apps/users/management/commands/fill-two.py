from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from apps.users.factory import UserFactory
from foodgram.utils.progress import Progress


class Command(BaseCommand):
    help = 'Creat "number" of users (default 30)'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int, default=3)

    def handle(self, *args, **options):
        n = options['number']
        users = UserFactory.create_batch(n)
        for user in users:
            try:
                user.save()
            except IntegrityError:
                n -= 1
                print(f'User {user} already exist. Skipping')

        Progress.report_success(n, 'Users')

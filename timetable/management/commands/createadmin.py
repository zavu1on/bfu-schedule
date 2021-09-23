from django.contrib.auth.models import User
from django.core.management import BaseCommand
from Schedule.settings import KEY_PASSWORD


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true')

    def handle(self, *args, **options):
        is_debug = bool(options['debug'])

        if is_debug:
            User.objects.create_superuser(
                username='admin',
                email=None,
                password='admin'
            )
        else:
            User.objects.create_superuser(
                username='admin',
                email=None,
                password=KEY_PASSWORD
            )

        self.stdout.write(self.style.SUCCESS('SuperUser created successfully!'))

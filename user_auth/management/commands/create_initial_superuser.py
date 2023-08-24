from django.core.management.base import BaseCommand
from user_auth.models import BoltUser

class Command(BaseCommand):
    help = 'Create an initial superuser'

    def handle(self, *args, **options):
        if not BoltUser.objects.filter(username='admin', email='a@a.com'):
            BoltUser.objects.create_superuser('admin', 'a@a.com', 'super_pass')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser "admin" already exists'))

from django.core.management.base import BaseCommand
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Create a super admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for super admin')
        parser.add_argument('--email', type=str, help='Email for super admin')
        parser.add_argument('--password', type=str, help='Password for super admin')

    def handle(self, *args, **options):
        username = options.get('username') or input('Enter username: ')
        email = options.get('email') or input('Enter email: ')
        password = options.get('password') or input('Enter password: ')

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'User with username "{username}" already exists')
            )
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='super'
        )

        self.stdout.write(
            self.style.SUCCESS(f'Super admin "{username}" created successfully')
        )
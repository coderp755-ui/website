from django.core.management.base import BaseCommand
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Create admin users with different roles'

    def handle(self, *args, **kwargs):
        # Create Super Admin
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_user(
                username='superadmin',
                email='super@admin.com',
                password='admin123',
                role='super',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Super Admin created: superadmin / admin123'))
        
        # Create Country Admin
        if not User.objects.filter(username='countryadmin').exists():
            User.objects.create_user(
                username='countryadmin',
                email='country@admin.com',
                password='admin123',
                role='country',
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS('Country Admin created: countryadmin / admin123'))
        
        # Create Branch Admin
        if not User.objects.filter(username='branchadmin').exists():
            User.objects.create_user(
                username='branchadmin',
                email='branch@admin.com',
                password='admin123',
                role='branch',
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS('Branch Admin created: branchadmin / admin123'))

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Setup production environment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser if one does not exist',
        )
        parser.add_argument(
            '--seed-data',
            action='store_true',
            help='Load initial seed data',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up production environment...'))

        if options['create_superuser']:
            self.create_superuser()

        if options['seed_data']:
            self.seed_data()

        self.stdout.write(self.style.SUCCESS('Production setup completed!'))

    def create_superuser(self):
        """Create a superuser if one doesn't exist"""
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@floods.pk')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'changeme123')
            
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser already exists, skipping creation.')
            )

    def seed_data(self):
        """Load initial seed data"""
        from django.core.management import call_command
        try:
            call_command('seed_data')
            self.stdout.write(self.style.SUCCESS('Seed data loaded successfully!'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading seed data: {e}')
            )

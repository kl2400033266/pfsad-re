from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or update an admin/superuser account.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--email', required=True)
        parser.add_argument('--password', required=True)

    def handle(self, *args, **options):
        username = options['username'].strip()
        email = options['email'].strip().lower()
        password = options['password']

        if not username:
            raise CommandError('Username cannot be empty.')

        if not email:
            raise CommandError('Email cannot be empty.')

        user_model = get_user_model()

        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )

        user.email = email
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated admin user: {username}'))

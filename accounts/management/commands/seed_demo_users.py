from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from support.models import CaseAssignment, HelpRequest


class Command(BaseCommand):
    help = 'Create demo users and sample assigned help requests for the PS04 project.'

    def handle(self, *args, **options):
        user_model = get_user_model()

        demo_users = [
            {
                'username': 'Mohan',
                'password': 'Mohan2006@',
                'role': 'admin',
                'email': 'mohan@example.com',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'raju',
                'password': 'common',
                'role': 'survivor',
                'email': 'raju@example.com',
            },
            {
                'username': 'Karthik',
                'password': 'common',
                'role': 'counsellor',
                'email': 'karthik@example.com',
            },
            {
                'username': 'nakul',
                'password': 'common',
                'role': 'legal_advisor',
                'email': 'nakul@example.com',
            },
        ]

        created_users = {}

        with transaction.atomic():
            for user_data in demo_users:
                user, _ = user_model.objects.get_or_create(username=user_data['username'])
                user.email = user_data['email']
                user.role = user_data['role']
                user.is_active = True
                user.is_staff = user_data.get('is_staff', False)
                user.is_superuser = user_data.get('is_superuser', False)
                user.set_password(user_data['password'])
                user.save()
                created_users[user.username] = user

            survivor = created_users['raju']
            counsellor = created_users['Karthik']
            legal_advisor = created_users['nakul']

            sample_requests = [
                {
                    'title': 'Urgent safety planning support',
                    'description': 'Need immediate confidential guidance and safe next steps.',
                    'category': 'physical',
                    'urgency_level': 'high',
                },
                {
                    'title': 'Legal protection advice',
                    'description': 'Need help understanding protection options and legal remedies.',
                    'category': 'legal',
                    'urgency_level': 'medium',
                },
            ]

            for request_data in sample_requests:
                help_request, _ = HelpRequest.objects.get_or_create(
                    survivor=survivor,
                    title=request_data['title'],
                    defaults={
                        'description': request_data['description'],
                        'category': request_data['category'],
                        'urgency_level': request_data['urgency_level'],
                        'status': 'assigned',
                        'is_confidential': True,
                    },
                )

                help_request.description = request_data['description']
                help_request.category = request_data['category']
                help_request.urgency_level = request_data['urgency_level']
                help_request.status = 'assigned'
                help_request.is_confidential = True
                help_request.save()

                CaseAssignment.objects.update_or_create(
                    help_request=help_request,
                    defaults={
                        'counsellor': counsellor,
                        'legal_advisor': legal_advisor,
                        'assigned_by': created_users['Mohan'],
                    },
                )

        self.stdout.write(self.style.SUCCESS('Demo users and sample requests have been created or updated.'))
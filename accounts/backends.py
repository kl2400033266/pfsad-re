from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get('username') or kwargs.get('email')
        if not identifier or not password:
            return None

        user_model = get_user_model()

        if '@' in identifier:
            candidate_users = user_model.objects.filter(
                Q(email__iexact=identifier) | Q(username__iexact=identifier)
            )
        else:
            candidate_users = user_model.objects.filter(username__iexact=identifier)

        for user in candidate_users:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        return None
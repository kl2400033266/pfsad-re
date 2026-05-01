import os
from django.contrib.auth import get_user_model


def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def ensure_bootstrap_admin():
    if not _env_bool('ADMIN_BOOTSTRAP_ENABLED', default=True):
        return None

    username = os.getenv('ADMIN_BOOTSTRAP_USERNAME', 'admin').strip()
    email = os.getenv('ADMIN_BOOTSTRAP_EMAIL', 'admin@example.com').strip().lower()
    password = os.getenv('ADMIN_BOOTSTRAP_PASSWORD', 'Admin@12345')
    force_reset = _env_bool('ADMIN_BOOTSTRAP_FORCE_PASSWORD_RESET', default=True)

    if not username or not password:
        return None

    user_model = get_user_model()

    user = user_model.objects.filter(username__iexact=username).first()
    if user is None and email:
        user = user_model.objects.filter(email__iexact=email).first()

    created = False
    if user is None:
        user = user_model.objects.create(
            username=username,
            email=email or None,
            role='admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        created = True

    user.role = 'admin'
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    if email:
        user.email = email

    if created or force_reset:
        user.set_password(password)

    user.save()
    return user

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    email = models.EmailField(
        blank=True,
        null=True
    )

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('survivor', 'Survivor'),
        ('counsellor', 'Counsellor'),
        ('legal_advisor', 'Legal Advisor'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
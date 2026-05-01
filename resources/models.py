from django.db import models
from django.conf import settings


class Resource(models.Model):

    RESOURCE_TYPE_CHOICES = (
        ('legal', 'Legal Resource'),
        ('counselling', 'Counselling Resource'),
        ('emergency', 'Emergency Contact'),
    )

    title = models.CharField(max_length=255)
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES
    )

    content = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.resource_type})"
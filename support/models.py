from django.db import models
from django.conf import settings


class HelpRequest(models.Model):

    CATEGORY_CHOICES = (
        ('physical', 'Physical Abuse'),
        ('emotional', 'Emotional Abuse'),
        ('financial', 'Financial Abuse'),
        ('legal', 'Legal Protection'),
    )

    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('closed', 'Closed'),
    )

    survivor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='help_requests'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_confidential = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.survivor.username}"
    
class CaseAssignment(models.Model):

    help_request = models.OneToOneField(
        HelpRequest,
        on_delete=models.CASCADE,
        related_name='assignment'
    )

    counsellor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_counsellor_cases'
    )

    legal_advisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_legal_cases'
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_by_admin'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assignment for {self.help_request.title}"
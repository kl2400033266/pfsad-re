from django.db import models
from django.conf import settings
from support.models import HelpRequest
import base64


class Message(models.Model):

    help_request = models.ForeignKey(
        HelpRequest,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    content = models.TextField()
    is_read = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Simulated encryption (for academic demonstration)
        if not self.pk:
            encoded = base64.b64encode(self.content.encode()).decode()
            self.content = encoded
        super().save(*args, **kwargs)

    def get_decoded_message(self):
        try:
            return base64.b64decode(self.content.encode()).decode()
        except:
            return self.content

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
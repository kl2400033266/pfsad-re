from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('help_request', 'sender', 'receiver', 'timestamp', 'is_read')
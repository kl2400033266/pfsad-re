from django.contrib import admin
from .models import HelpRequest, CaseAssignment


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'survivor', 'category', 'urgency_level', 'status', 'created_at')
    list_filter = ('status', 'category', 'urgency_level')


@admin.register(CaseAssignment)
class CaseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('help_request', 'counsellor', 'legal_advisor', 'assigned_at')
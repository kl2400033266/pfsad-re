from django import forms
from .models import HelpRequest, CaseAssignment
from django.contrib.auth import get_user_model


class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = ['title', 'description', 'category', 'urgency_level', 'is_confidential']


User = get_user_model()


class CaseAssignmentForm(forms.ModelForm):
    class Meta:
        model = CaseAssignment
        fields = ['counsellor', 'legal_advisor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['counsellor'].queryset = User.objects.filter(role='counsellor', is_active=True)
        self.fields['legal_advisor'].queryset = User.objects.filter(role='legal_advisor', is_active=True)
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SurvivorRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            return None

        user_model = get_user_model()
        existing_user = user_model.objects.filter(email__iexact=email).first()
        if existing_user:
            raise forms.ValidationError(
                'An account with this email already exists. Please log in instead.'
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'survivor'
        user.is_verified = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')


class ProfessionalCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('counsellor', 'Counsellor'),
        ('legal_advisor', 'Legal Advisor'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False, max_length=15)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'role', 'password1', 'password2']

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            return None

        user_model = get_user_model()
        existing_user = user_model.objects.filter(email__iexact=email).first()
        if existing_user:
            raise forms.ValidationError('A user with this email already exists.')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.is_verified = True

        if commit:
            user.save()

        return user


class ProfessionalUpdateForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('counsellor', 'Counsellor'),
        ('legal_advisor', 'Legal Advisor'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False, max_length=15)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'role', 'is_active']

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            return None

        user_model = get_user_model()
        existing_user = user_model.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).first()
        if existing_user:
            raise forms.ValidationError('A user with this email already exists.')

        return email
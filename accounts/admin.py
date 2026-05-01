from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('role', 'phone_number', 'is_verified')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
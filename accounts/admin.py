from django.contrib import admin
from .models import CustomUser, Role, Team
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'team' 'First Name', 'Last Name', 'is_staff', 'is_active',]

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("role", "team")}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("role", "team")}),
    )

admin.site.register(CustomUser)
admin.site.register([Role, Team])





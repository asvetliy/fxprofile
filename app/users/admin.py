from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserRegistrationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserRegistrationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'birth_date', 'password1', 'password2',
                'country', 'city', 'promo', 'phone', 'is_active', 'is_staff', 'is_superuser', 'is_verified',
            )
        }
         ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'birth_date', 'phone', 'promo', )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_verified', ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
    )
    list_display = ('username', 'email', 'country', 'is_active', 'is_staff', 'promo', )
    list_per_page = 20

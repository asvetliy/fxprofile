from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .forms import UserRegistrationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserRegistrationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'birth_date', 'password1', 'password2',
                'country', 'city', 'promo', 'phone', 'is_active', 'is_staff', 'is_superuser', 'is_verified',
                'email_confirmed',
            )
        }
         ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'country', 'city', 'birth_date', 'phone', 'promo',)}),
        (_('Permissions'), {
            'fields': (
                'email_confirmed', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                'is_verified',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    list_display = ('username', 'email', 'country_with_flag', 'is_active', 'is_staff', 'promo', 'date_joined',)
    list_per_page = 20
    ordering = ('-date_joined',)

    def country_with_flag(self, obj: User):
        return format_html(
            f'<img src="{obj.country.flag}" style="{obj.country.flag_css}" alt="{obj.country.name}"> {obj.country.name}')

    country_with_flag.admin_order_field = 'country'
    country_with_flag.short_description = 'country'

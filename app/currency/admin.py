from django.contrib import admin
from .models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('iso', 'symbol', 'name', 'digest', 'is_default', 'is_base', 'is_enabled')

from django.contrib import admin

from .models import PaymentSystem


@admin.register(PaymentSystem)
class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'cls', 'is_enabled', 'withdraw', 'config', )
    list_per_page = 20

from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from .models import PaymentSystem, EportalWallet, BlockchainWallet


@admin.register(PaymentSystem)
class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'cls', 'is_enabled', 'withdraw', 'config', )
    list_per_page = 20
    readonly_fields = ('cls', 'code', )
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget(width='100%', height='300px')},
    }


@admin.register(EportalWallet)
class EportalWalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ewallet', )
    autocomplete_fields = ('user', )
    search_fields = ('ewallet', 'user__username', )
    list_per_page = 20


@admin.register(BlockchainWallet)
class BlockchainWalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'bwallet', 'expired_at', 'picked_at', )
    autocomplete_fields = ('transaction', )
    search_fields = ('bwallet', )
    list_per_page = 20

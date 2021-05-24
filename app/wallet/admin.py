from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Transaction, Wallet


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'transaction_amount', 'user_username', 'type', 'status', 'from_to_wallet', 'created_at', )
    list_filter = ('type', 'status', 'created_at', )
    autocomplete_fields = ('wallet', 'user', )
    search_fields = ('wallet__user__username', 'id', )
    list_per_page = 20

    def user_username(self, obj: Transaction):
        url = reverse('admin:users_user_change', args=(obj.wallet.user_id, ))
        return format_html(f'<a href="{url}">{obj.wallet.user.username}</a>')

    user_username.admin_order_field = 'user'
    user_username.short_description = 'user'

    def transaction_amount(self, obj: Transaction):
        return obj.transaction_amount

    transaction_amount.admin_order_field = 'amount'
    transaction_amount.short_description = 'amount'


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username', 'wallet_balance', 'currency', 'created_at', )
    autocomplete_fields = ('user', )
    search_fields = ('user__username', )
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def wallet_balance(self, obj: Wallet):
        return obj.get_balance()

    wallet_balance.admin_order_field = 'balance'
    wallet_balance.short_description = 'balance'

    def user_username(self, obj: Wallet):
        url = reverse('admin:users_user_change', args=(obj.user_id, ))
        return format_html(f'<a href="{url}">{obj.user.username}</a>')

    user_username.admin_order_field = 'user'
    user_username.short_description = 'user'

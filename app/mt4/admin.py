from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import UserAccounts, Accounts, Prices


@admin.register(UserAccounts)
class UserAccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username', 'pwd', 'inv_pwd', 'phone_pwd', 'account_type', 'currency', )
    autocomplete_fields = ('user', )
    search_fields = ('user__username', 'id', )
    list_per_page = 20

    def user_username(self, obj: UserAccounts):
        url = reverse('admin:users_user_change', args=(obj.user_id, ))
        return format_html(f'<a href="{url}">{obj.user.username}</a>')

    user_username.admin_order_field = 'user'
    user_username.short_description = 'user'


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ('LOGIN', 'GROUP', 'BALANCE', 'EQUITY', 'MARGIN', )
    search_fields = ('LOGIN', )
    list_per_page = 20


@admin.register(Prices)
class PricesAdmin(admin.ModelAdmin):
    list_display = ('SYMBOL', 'BID', 'ASK', 'LOW', 'HIGH', 'MODIFY_TIME', )
    search_fields = ('SYMBOL', )
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

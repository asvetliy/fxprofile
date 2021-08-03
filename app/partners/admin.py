import csv

from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone

from rangefilter.filters import DateRangeFilter
from math_helper import int_to_amount

from .models import *
from .forms import PartnerTransactionAdminForm


class CardInline(admin.TabularInline):
    model = Card

    def has_view_permission(self, request, obj=None):
        return True


class VerificationInline(admin.TabularInline):
    model = Verification
    fields = ('boolean_declaration', 'boolean_identification', 'boolean_invoice', )
    readonly_fields = ('boolean_declaration', 'boolean_identification', 'boolean_invoice', )

    def has_view_permission(self, request, obj=None):
        return True

    def boolean_declaration(self, obj: Verification):
        return bool(obj.declaration)

    boolean_declaration.admin_order_field = 'declaration'
    boolean_declaration.short_description = 'declaration'
    boolean_declaration.boolean = True

    def boolean_identification(self, obj: Verification):
        return bool(obj.identification)

    boolean_identification.admin_order_field = 'identification'
    boolean_identification.short_description = 'identification'
    boolean_identification.boolean = True

    def boolean_invoice(self, obj: Verification):
        return bool(obj.invoice)

    boolean_invoice.admin_order_field = 'invoice'
    boolean_invoice.short_description = 'invoice'
    boolean_invoice.boolean = True


class VerificationRequestInline(admin.TabularInline):
    model = VerificationRequest
    exclude = ('file', )

    def has_view_permission(self, request, obj=None):
        return True


class WalletInline(admin.TabularInline):
    model = Wallet
    fields = ('currency', 'wallet_balance', )
    readonly_fields = ('wallet_balance', )

    def has_view_permission(self, request, obj=None):
        return True

    def wallet_balance(self, obj: Wallet):
        return obj.get_balance()

    wallet_balance.admin_order_field = 'balance'
    wallet_balance.short_description = 'balance'


class TransactionInline(admin.TabularInline):
    model = Transaction

    fields = ('wallet', 'type', 'transaction_amount', 'from_to_wallet', 'status', 'description', )
    readonly_fields = ('transaction_amount', )

    def has_view_permission(self, request, obj=None):
        return True

    def transaction_amount(self, obj: Transaction):
        return obj.transaction_amount

    transaction_amount.admin_order_field = 'amount'
    transaction_amount.short_description = 'amount'


@admin.register(PartnerUser)
class PartnerUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'email_confirmed', 'is_verified', 'date_joined', )
    list_filter = ('is_verified', 'date_joined', )
    list_display_links = ('username', )
    search_fields = ('username', 'email', )
    inlines = (VerificationInline, CardInline, VerificationRequestInline, WalletInline, TransactionInline, )
    exclude = ('is_staff', 'password', 'groups', 'user_permissions', 'avatar', 'birth_date', 'about_me', 'is_superuser', )
    list_per_page = 20

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        if request.user.promo:
            return self.model.objects.filter(promo=request.user.promo, is_staff=0)
        return self.model.objects.all()


@admin.register(PartnerTransaction)
class PartnerTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username', 'wallet', 'type', 'transaction_amount', 'from_to_wallet', 'status', 'description', 'user_promo', )
    search_fields = ('user__username', 'id', 'user__promo', )
    list_filter = ('user__groups__name', 'type', 'status', ('created_at', DateRangeFilter), )
    list_per_page = 20
    actions = ['export_as_csv']
    readonly_fields = ['created_at']
    form = PartnerTransactionAdminForm

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}-{timezone.now().timestamp()}.csv'

        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            obj.amount = int_to_amount(obj.amount, obj.wallet.currency.digest)
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    export_as_csv.short_description = "Export as CSV"

    def user_promo(self, obj: Wallet):
        return obj.user.promo

    user_promo.admin_order_field = 'promo'
    user_promo.short_description = 'promo'

    def user_username(self, obj: Wallet):
        url = reverse('admin:users_user_change', args=(obj.user_id, ))
        return format_html(f'<a href="{url}">{obj.user.username}</a>')

    user_username.admin_order_field = 'user'
    user_username.short_description = 'user'

    def transaction_amount(self, obj: Transaction):
        return obj.transaction_amount

    transaction_amount.admin_order_field = 'amount'
    transaction_amount.short_description = 'amount'

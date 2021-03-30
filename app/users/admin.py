from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.apps import apps
from django.utils.translation import gettext_lazy as _

from .forms import UserRegistrationForm
from .models import User, PartnerUser

Transaction = apps.get_model('wallet', 'Transaction')
Wallet = apps.get_model('wallet', 'Wallet')
Verification = apps.get_model('verification', 'Verification')
VerificationRequest = apps.get_model('verification', 'VerificationRequest')
Card = apps.get_model('verification', 'Card')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserRegistrationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                'country', 'city', 'promo', 'phone', 'is_active', 'is_staff', 'is_superuser',
            )
        }
         ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'promo', )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
    )
    list_display = ('username', 'email', 'country', 'is_active', 'is_staff', 'promo', )
    list_per_page = 20


class CardInline(admin.TabularInline):
    model = Card


class VerificationInline(admin.TabularInline):
    model = Verification
    fields = ('boolean_declaration', 'boolean_identification', 'boolean_invoice', )
    readonly_fields = ('boolean_declaration', 'boolean_identification', 'boolean_invoice', )

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


class WalletInline(admin.TabularInline):
    model = Wallet
    fields = ('currency', 'wallet_balance', )
    readonly_fields = ('wallet_balance', )

    def wallet_balance(self, obj: Wallet):
        return obj.get_balance()

    wallet_balance.admin_order_field = 'balance'
    wallet_balance.short_description = 'balance'


class TransactionInline(admin.TabularInline):
    model = Transaction

    fields = ('wallet', 'type', 'transaction_amount', 'from_to_wallet', 'status', 'description', )
    readonly_fields = ('transaction_amount', )

    def transaction_amount(self, obj: Transaction):
        return obj.transaction_amount

    transaction_amount.admin_order_field = 'amount'
    transaction_amount.short_description = 'amount'


@admin.register(PartnerUser)
class PartnerUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'email_confirmed', 'is_verificated', 'date_joined', )
    list_filter = ('is_verificated', 'date_joined', )
    list_display_links = ('username', )
    search_fields = ('username', 'email', )
    inlines = (VerificationInline, CardInline, VerificationRequestInline, WalletInline, TransactionInline, )
    exclude = ('is_staff', 'password', 'groups', 'user_permissions', 'avatar', 'birth_date', 'about_me', 'is_superuser', )

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

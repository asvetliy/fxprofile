from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import VerificationRequest, Card, Verification


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'old_file_name', 'file', 'type', 'status', 'updated_at', 'created_at', )
    autocomplete_fields = ('user', 'card', )
    list_filter = ('type', 'status', 'updated_at', 'created_at', )
    list_per_page = 20
    list_display_links = ('id', 'old_file_name', )
    search_fields = ('id', 'user__username', )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'number', 'is_verified', )
    autocomplete_fields = ('user', )
    list_filter = ('is_verified', )
    list_per_page = 20
    list_display_links = ('id', 'number', )
    search_fields = ('number', 'user__username', )


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'dd', 'ident', 'inv', )
    list_per_page = 20
    autocomplete_fields = ('user', 'declaration', 'identification', 'invoice', )
    search_fields = ('user__username', 'id', )

    def dd(self, obj: Verification):
        if obj.declaration is None:
            return None
        url = reverse('admin:verification_verificationrequest_change', args=(obj.declaration_id, ))
        return format_html(f'<a href="{url}">{obj.declaration.status}</a>')

    dd.admin_order_field = 'declaration'
    dd.short_description = 'declaration'

    def ident(self, obj: Verification):
        if obj.identification is None:
            return None
        url = reverse('admin:verification_verificationrequest_change', args=(obj.identification_id, ))
        return format_html(f'<a href="{url}">{obj.identification.status}</a>')

    ident.admin_order_field = 'identification'
    ident.short_description = 'identification'

    def inv(self, obj: Verification):
        if obj.invoice is None:
            return None
        url = reverse('admin:verification_verificationrequest_change', args=(obj.invoice_id, ))
        return format_html(f'<a href="{url}">{obj.invoice.status}</a>')

    inv.admin_order_field = 'invoice'
    inv.short_description = 'invoice'

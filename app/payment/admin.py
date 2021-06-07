from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from .models import PaymentSystem


@admin.register(PaymentSystem)
class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'cls', 'is_enabled', 'withdraw', 'config', )
    list_per_page = 20
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget(width='100%', height='300px')},
    }

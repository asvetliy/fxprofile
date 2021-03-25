from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from .models import QuestionMessage, QuestionRequest


@admin.register(QuestionRequest)
class QuestionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username', 'messages', 'status', 'updated_at', 'created_at', )
    autocomplete_fields = ('user', )
    search_fields = ('user__username', 'id', )
    list_per_page = 20
    list_filter = ('status', 'created_at', 'updated_at', )

    def user_username(self, obj: QuestionRequest):
        url = reverse('admin:users_user_change', args=(obj.user_id, ))
        return format_html(f'<a href="{url}">{obj.user.username}</a>')

    user_username.admin_order_field = 'user'
    user_username.short_description = 'user'

    def messages(self, obj: QuestionRequest):
        url = reverse('admin:questions_questionmessage_changelist') + '?' + urlencode({'q': str(obj.id)})
        return format_html(f'<a href="{url}">Show messages</a>')

    messages.admin_order_field = 'messages'
    messages.short_description = 'messages'


@admin.register(QuestionMessage)
class QuestionMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username', 'request_id', 'status', 'text', 'created_at', )
    autocomplete_fields = ('user', 'request')
    search_fields = ('user__username', 'id', 'request__id', )
    list_per_page = 10
    list_filter = ('status', 'created_at', )

    def user_username(self, obj: QuestionMessage):
        url = reverse('admin:users_user_change', args=(obj.user_id, ))
        return format_html(f'<a href="{url}">{obj.user.username}</a>')

    user_username.admin_order_field = 'user'
    user_username.short_description = 'user'

    def request_id(self, obj: QuestionMessage):
        url = reverse('admin:questions_questionrequest_change', args=(obj.request.id, ))
        return format_html(f'<a href="{url}">{obj.request.id}</a>')

    request_id.admin_order_field = 'request'
    request_id.short_description = 'request'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user.id
        return form

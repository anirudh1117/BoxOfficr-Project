from django.contrib import admin
from .models import LogEntry
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag',
    ]

    search_fields = [
        'object_repr',
        'change_message',
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == 1:  # Addition
            link = reverse('admin:%s_%s_change' % (obj.content_type.app_label, obj.content_type.model),  args=[obj.object_id] )
        elif obj.action_flag == 2:  # Change
            link = reverse('admin:%s_%s_change' % (obj.content_type.app_label, obj.content_type.model),  args=[obj.object_id] )
        else:  # Deletion
            link = None

        if link:
            return mark_safe('<a href="%s">%s</a>' % (link, escape(obj.object_repr)))
        else:
            return escape(obj.object_repr)

    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

admin.site.register(LogEntry, LogEntryAdmin)

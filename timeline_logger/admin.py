from django.contrib import admin


from .models import TimelineLog


@admin.register(TimelineLog)
class TimelineLogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp', 'template']
    list_filter = ['timestamp', 'content_type']
    list_select_related = ['content_type']

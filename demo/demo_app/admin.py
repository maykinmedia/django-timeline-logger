from django.contrib import admin

from import_export.admin import ExportMixin
from timeline_logger.models import TimelineLog
from timeline_logger.admin import TimelineLogAdmin

admin.site.unregister(TimelineLog)


@admin.register(TimelineLog)
class TimelineLogAdmin(ExportMixin, TimelineLogAdmin):
    pass

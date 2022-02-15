from django.contrib import admin

from import_export.admin import ExportMixin
from import_export.formats import base_formats
from import_export_xml.formats import XML

from timeline_logger.admin import TimelineLogAdmin
from timeline_logger.models import TimelineLog
from timeline_logger.resources import TimelineLogResource

admin.site.unregister(TimelineLog)


@admin.register(TimelineLog)
class TimelineLogAdmin(ExportMixin, TimelineLogAdmin):
    formats = (
        XML,
        base_formats.CSV,
        base_formats.XLS,
        base_formats.XLSX,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    resource_class = TimelineLogResource

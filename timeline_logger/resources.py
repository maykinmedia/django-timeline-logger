from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import Widget

from .models import TimelineLog


class JSONWidget(Widget):
    def render(self, value, obj=None):
        return value


class TimelineLogResource(ModelResource):
    extra_data = Field(
        attribute="extra_data",
        column_name="extra_data",
        widget=JSONWidget(),
        default=None,
    )

    class Meta:
        model = TimelineLog

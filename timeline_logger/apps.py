from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TimelineLoggerConfig(AppConfig):
    name = "timeline_logger"
    verbose_name = _("Django Timeline Logger")
    default_auto_field = "django.db.models.fields.BigAutoField"

    def ready(self):
        from . import conf  # noqa

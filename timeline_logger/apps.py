from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TimelineLoggerConfig(AppConfig):
    name = 'timeline_logger'
    verbose_name = _('Django Timeline Logger')

    def ready(self):
        from . import conf  # noqa

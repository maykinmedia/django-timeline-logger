from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


class TimelineLoggerConf(AppConf):
    class Meta:
        prefix = 'timeline'

from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


class TimelineLoggerConf(AppConf):
    TIMELINE_ACTIONS = (
        ('created', _('Created')),
        ('deleted', _('Deleted')),
        ('updated', _('Updated')),
        ('related', _('Related'))
    )

    class Meta:
        prefix = 'timeline'

    def configure_timeline_actions(self, value):
        if value is None:
            raise ImproperlyConfigured(
                'Missing setting TIMELINE_ACTIONS must be defined in order to'
                'set which actions towards models are available.'
            )

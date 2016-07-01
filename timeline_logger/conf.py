from __future__ import unicode_literals

from django.conf import settings  # noqa
from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


class TimelineLoggerConf(AppConf):

    DEFAULT_TEMPLATE = 'timeline_logger/default.txt'

    PAGINATE_BY = 25

    USER_EMAIL_FIELD = 'email'

    DIGEST_EMAIL_RECIPIENTS = None
    DIGEST_EMAIL_SUBJECT = _('Events timeline')
    DIGEST_FROM_EMAIL = None

    class Meta:
        prefix = 'timeline'

    def configure_digest_email_recipients(self, value):
        if value is None:
            return []
        return value

    def configure_digest_from_email(self, value):
        if value is None:
            return settings.DEFAULT_FROM_EMAIL
        return value

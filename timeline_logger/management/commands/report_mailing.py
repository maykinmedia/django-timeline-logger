import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from timeline_logger.compat import html
from timeline_logger.models import TimelineLog


logger = logging.getLogger('timeline_logger')


class Command(BaseCommand):
    help = 'Sends mail notifications for last events to (admin) users.'
    template_name = 'timeline_logger/notifications.html'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days', type=int,
            help='An integer number with the number of days to look at from today to the past.'
        )

        recipients_group = parser.add_mutually_exclusive_group()
        recipients_group.add_argument('--all', action='store_true', help=_('Send e-mail to all users'))
        recipients_group.add_argument('--staff', action='store_true', help=_('Send e-mail to staff users'))
        recipients_group.add_argument(
            '--recipients-from-setting', action='store_true',
            help=_('Send e-mail to adresses listed in settings.TIMELINE_DIGEST_EMAIL_RECIPIENTS')
        )

    def handle(self, *args, **options):
        recipients = self.get_recipients(**options)
        queryset = self.get_queryset(**options)

        if not queryset.exists():
            logger.info('No logs in timeline. No emails sent.')
            return

        self.send_email(recipients, queryset)

    def get_queryset(self, **options):
        """
        Filters the list of log objects to display
        """
        days = options.get('days')
        queryset = TimelineLog.objects.order_by('-timestamp')
        if days:
            try:
                start = timezone.now() - timedelta(days=days)
            except TypeError:
                raise CommandError("Incorrect 'days' parameter. 'days' must be a number of days.")
            else:
                return queryset.filter(timestamp__gte=start)

        return queryset

    def get_recipients(self, **options):
        """
        Figures out the recipients
        """
        if options['recipients_from_setting']:
            return settings.TIMELINE_DIGEST_EMAIL_RECIPIENTS

        users = get_user_model()._default_manager.all()
        if options['staff']:
            users = users.filter(is_staff=True)
        elif not options['all']:
            users = users.filter(is_staff=True, is_superuser=True)
        return users.values_list(settings.TIMELINE_USER_EMAIL_FIELD, flat=True)

    def get_context(self, queryset):
        return {
            'logs': queryset,
            'start_date': queryset[0].timestamp,
        }

    def send_email(self, recipients, queryset):
        context = self.get_context(queryset)
        html_content = render_to_string(self.template_name, context)
        text_content = html.unescape(strip_tags(html_content))

        send_mail(
            subject=settings.TIMELINE_DIGEST_EMAIL_SUBJECT,
            message=text_content,
            from_email=settings.TIMELINE_DIGEST_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
            html_message=html_content
        )
        logger.info('Notification emails sent to: %s', recipients)

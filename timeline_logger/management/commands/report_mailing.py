import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _

from timeline_logger.models import TimelineLog


logger = logging.getLogger('timeline_logger')


class Command(BaseCommand):
    help = 'Sends mail notifications for last events to (admin) users.'

    def add_arguments(self, parser):
        parser.add_argument('--staff', action='store_true', default=False, help='Send emails only to staff users.')
        parser.add_argument('--all', action='store_true', default=False, help="Send emails to all users (overrides 'staff').")
        parser.add_argument('--days', type=str, help='An integer number with the number of days to look at from today.')

    def handle(self, *args, **options):
        staff_only = options.get('staff', False)
        all_users = options.get('all', False)
        days = options.get('days')
        User = get_user_model()

        if days:
            try:
                start = datetime.today().date() - timedelta(days=days)
            except TypeError:
                raise CommandError("Incorrect 'start' parameter. 'start' must be a number of days.")

            logs = TimelineLog.objects.filter(timestamp__gte=start).order_by('-timestamp')
        else:
            logs = TimelineLog.objects.order_by('-timestamp')

        if not logs:
            logger.info('No logs in timeline. No emails sent.')
            return

        start_date = logs[0].timestamp.strftime('%Y-%m-%d')

        if all_users:
            receivers = User.objects.all()
        elif staff_only:
            receivers = User.objects.filter(is_staff=True)
        else:
            receivers = User.objects.filter(is_superuser=True)

        receivers = receivers.values_list('email', flat=True)

        context = {'logs': logs, 'start_date': start_date}
        html_content = render_to_string('timeline_logger/notifications.html', context)
        text_content = strip_tags(html_content)

        send_mail(
            subject=_('Events timeline'),
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=receivers,
            fail_silently=False,
            html_message=html_content
        )
        logger.info(
            'Notification emails sent to: {0}'.format(', '.join(receivers)))


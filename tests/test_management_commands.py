from datetime import timedelta

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from django.conf import settings
from django.core import mail
from django.core.management import call_command, CommandError
from django.test import override_settings, TestCase
from django.utils import timezone

from timeline_logger.models import TimelineLog
from .factories import ArticleFactory, UserFactory


class ReportMailingTestCase(TestCase):
    def setUp(self):
        self.article = ArticleFactory.create()

        self.user = UserFactory.create(email='jose@maykinmedia.nl')
        self.staff_user = UserFactory.create(is_staff=True)
        self.admin_user = UserFactory.create(is_staff=True, is_superuser=True)

        self.log_1 = TimelineLog.objects.create(
            content_object=self.article,
            user=self.user,
        )
        self.log_2 = TimelineLog.objects.create(
            content_object=self.article,
            user=self.user,
        )
        self.log_3 = TimelineLog.objects.create(
            content_object=self.article,
            user=self.user,
        )

    @override_settings(TIMELINE_DIGEST_EMAIL_RECIPIENTS=['jose@maykinmedia.nl'])
    def test_recipients_from_setting_parameter(self):
        """
        The ``--recipients-from-setting`` parameter will send notifications
        only to those users listed in the ``TIMELINE_DIGEST_EMAIL_RECIPIENTS``
        setting.
        """
        call_command('report_mailing', '--recipients-from-setting')

        self.assertEqual(len(mail.outbox), 1)
        self.assertListEqual(mail.outbox[0].to, settings.TIMELINE_DIGEST_EMAIL_RECIPIENTS)

    def test_staff_parameter(self):
        """
        The ``--staff`` parameter will send notifications only to those users
        marked who have ``is_staff=True``.
        """
        call_command('report_mailing', '--staff')

        self.assertEqual(len(mail.outbox), 1)
        self.assertListEqual(mail.outbox[0].to, [self.staff_user.email, self.admin_user.email])

    def test_all_parameter(self):
        """
        The ``--all`` parameter will send notifications to all users.
        """
        call_command('report_mailing', '--all')

        self.assertEqual(len(mail.outbox), 1)
        self.assertListEqual(mail.outbox[0].to, [self.user.email, self.staff_user.email, self.admin_user.email])

    def test_no_recipients_parameter(self):
        """
        When no 'recipients' parameter is passed, only those users who are
        'staff' and 'superuser' will be notified.
        """
        call_command('report_mailing')

        self.assertEqual(len(mail.outbox), 1)
        self.assertListEqual(mail.outbox[0].to, [self.admin_user.email])

    def test_invalid_days_parameter(self):
        """
        The ``--days`` parameter must be an integer, representing the number of
        days until today.
        """
        self.assertRaisesMessage(
            CommandError,
            "Incorrect 'days' parameter. 'days' must be a number of days.",
            call_command,
            'report_mailing', days='NaN'
        )

    def test_days_parameter_successful(self):
        """
        The ``--days`` parameter will restrict the logs to only those generated
        from today until the number of days before passed in the parameter.
        """
        # Change the timestamp of the existing logs in order to test this.
        self.log_1.timestamp = timezone.now() - timedelta(days=30)
        self.log_2.timestamp = timezone.now() - timedelta(days=10)
        self.log_1.save()
        self.log_2.save()

        call_command('report_mailing', days=15)

        self.assertEqual(len(mail.outbox), 1)

        # The 1st log `self.log_1` is NOT present in the email, because it was
        # generated before 15 days ago from today.
        self.assertNotIn(self.log_1.timestamp.strftime('%b. %-d, %Y'), mail.outbox[0].body)

        # The other logs `self.log_2` and `self.log_3` are properly
        self.assertIn(self.log_2.timestamp.strftime('%b. %-d, %Y'), mail.outbox[0].body)
        self.assertIn(self.log_3.timestamp.strftime('%b. %-d, %Y'), mail.outbox[0].body)

    def test_no_logs_recorded(self):
        """
        The command will do nothing if there are no logs at all.
        """
        # Get rid of all the existent logs.
        TimelineLog.objects.all().delete()

        call_command('report_mailing')

        self.assertEqual(len(mail.outbox), 0)

    def test_no_timeline_digest_from_email_setting(self):
        """
        If the ``TIMELINE_DIGEST_FROM_EMAIL`` setting is not set, the backend
        will default to the Django's standard ``DEFAULT_FROM_EMAIL`` setting.
        """
        call_command('report_mailing')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    @override_settings(TIMELINE_DIGEST_FROM_EMAIL='reports@maykinmedia.nl')
    def test_timeline_digest_from_email_setting(self):
        """
        If the ``TIMELINE_DIGEST_FROM_EMAIL`` setting is not set, the backend
        will default to the Django's standard ``DEFAULT_FROM_EMAIL`` setting.
        """
        call_command('report_mailing')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, settings.TIMELINE_DIGEST_FROM_EMAIL)
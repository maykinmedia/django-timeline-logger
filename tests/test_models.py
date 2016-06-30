# -*- coding: utf-8 -*-

from unittest import skipIf

from django.conf import settings
from django.contrib.auth.models import User
from django.template.exceptions import TemplateDoesNotExist
from django.template.defaultfilters import date
from django.test import RequestFactory, TestCase

from timeline_logger.models import TimelineLog
from .factories import ArticleFactory


class TimelineLogTestCase(TestCase):
    def setUp(self):
        self.article = ArticleFactory.create()

        self.user = User.objects.create(username='john_doe', email='john.doe@maykinmedia.nl')

        self.timeline_log = TimelineLog.objects.create(
            content_object=self.article,
            user=self.user,
        )

        self.request = RequestFactory().get('/my_object/')

    def test_log_from_request_no_user(self):
        """
        Test ``log_from_request`` method when no user is passed in request.
        """
        log = TimelineLog.log_from_request(self.request, self.article)

        self.assertIsNone(log.user)

    def test_log_from_request_with_user(self):
        """
        Test ``log_from_request`` method when a user is passed in request.
        """
        self.request.user = self.user
        log = TimelineLog.log_from_request(self.request, self.article)

        self.assertEqual(log.user, self.user)

    @skipIf(settings.DATABASES['default']['ENGINE'] != 'django.db.backends.postgresql',
            "'JSONField' can only be used in a PostgreSQL database.")
    def test_log_from_request_no_extra_data(self):
        """
        Test ``log_from_request`` method when no ``extra_data`` dictionary is
        passed.
        """
        log = TimelineLog.log_from_request(self.request, self.article)

        self.assertIsNone(log.extra_data)

    @skipIf(settings.DATABASES['default']['ENGINE'] != 'django.db.backends.postgresql',
            "'JSONField' can only be used in a PostgreSQL database.")
    def test_log_from_request_with_extra_data(self):
        """
        Test ``log_from_request`` method when an ``extra_data`` dictionary is
        passed.
        """
        extra_data = {
            'status': 'published',
            'institution': 'Utrecht University'
        }

        log = TimelineLog.log_from_request(self.request, self.article, **extra_data)

        self.assertDictEqual(log.extra_data, extra_data)

    def test_log_from_request_no_template(self):
        """
        Test ``log_from_request`` method when no specific template is passed.
        """
        log = TimelineLog.log_from_request(self.request, self.article)

        self.assertEqual(log.template, 'timeline_logger/default.txt')

    def test_log_from_request_wrong_template(self):
        """
        ``log_from_request`` method will raise a ``TemplateDoesNotExist`` error
        exception when the passed template does not exist.
        """
        self.assertRaises(
            TemplateDoesNotExist,
            TimelineLog.log_from_request,
            self.request, self.article, 'non_existent.html'
        )

    def test_get_message(self):
        """
        Test the ``get_message`` method rendering a simple default log message.
        """
        log = TimelineLog.log_from_request(self.request, self.article)

        self.assertEqual(
            log.get_message(),
            '{0} - Anonymous user event on {1}.\n'.format(
                date(log.timestamp, 'DATETIME_FORMAT'),
                log.content_object
            )
        )

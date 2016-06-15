import logging

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible

from .conf import settings


logger = logging.getLogger('timeline_logger')


@python_2_unicode_compatible
class TimelineLog(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    extra_data = JSONField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    template = models.CharField(max_length=200, default='timeline_logger/default.txt')

    @classmethod
    def log_from_request(cls, request, content_object, **extra_data):
        """
        Given an ``HTTPRequest`` object and a generic content, it creates a
        ``TimelineLog`` object to store the data of that request.

        :param request: A Django ``HTTPRequest`` object.
        :param content_object: A Django model instance. Any object can be
        related.
        :param extra_data: A dictionary (translatable into JSON) determining
        specifications of the action performed.
        :return: A newly created ``TimelineLog`` instance.
        """
        user = request.user
        user = user if isinstance(user, User) else None

        timeline_log = cls.objects.create(
            content_object=content_object,
            extra_data=extra_data or None,
            user=user,
        )
        logger.debug('Logged event in {0} {1}.'.format(
            content_object._meta.object_name, content_object.pk))

        return timeline_log

    def get_message(self, template=None):
        """
        Gets the 'log' message, describing the event performed.

        :param template: String representing the template to be used to render
        the message. Defaults to ``self.template``.
        :return: The log message string.
        """
        return render_to_string(template or self.template, {'log': self})

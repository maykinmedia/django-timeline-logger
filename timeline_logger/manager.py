from django.contrib.contenttypes.models import ContentType
from django.db.models import Manager, Model


class TimelineLogManager(Manager):
    def for_object(self, obj: Model):
        content_type = ContentType.objects.get_for_model(obj)

        return self.filter(
            content_type=content_type,
            object_id=obj.pk,
        )

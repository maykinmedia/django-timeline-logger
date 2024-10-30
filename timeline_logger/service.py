from datetime import timedelta

from django.utils import timezone

from .models import TimelineLog


def prune_timeline_logs(*, keep_days: int | None = None) -> int:
    """Delete the timeline logs instances.

    :param keep_days: If specified, only delete records older than the specified number of days.
    :returns: The number of deleted instances.
    """
    limit = timezone.now()
    if keep_days is not None:
        limit -= timedelta(days=keep_days)

    number, _ = TimelineLog.objects.filter(timestamp__lte=limit).delete()
    return number

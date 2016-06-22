from django.conf import settings
from django.views.generic import ListView

from .models import TimelineLog


class TimelineLogListView(ListView):
    queryset = TimelineLog.objects.order_by('-timestamp')
    paginate_by = settings.TIMELINE_PAGINATE_BY

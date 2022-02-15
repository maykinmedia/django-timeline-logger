from django.urls import path

from .views import TimelineLogListView

app_name = "timeline"

urlpatterns = [
    path("", TimelineLogListView.as_view(), name="timeline"),
]

from django.conf.urls import url

from .views import TimelineLogListView


app_name = 'timeline'
urlpatterns = [
    url(r'^$', TimelineLogListView.as_view(), name='timeline'),
]

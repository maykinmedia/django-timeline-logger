from django.urls import include, path

urlpatterns = [
    path("", include("timeline_logger.urls")),
]

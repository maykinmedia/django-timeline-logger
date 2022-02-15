from pkg_resources import get_distribution

__version__ = get_distribution("django-timeline-logger").version

default_app_config = "timeline_logger.apps.TimelineLoggerConfig"

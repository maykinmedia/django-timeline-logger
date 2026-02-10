import logging
import logging.config
import time
import uuid
from collections.abc import Mapping
from contextlib import nullcontext
from dataclasses import dataclass
from unittest.mock import patch

from django.contrib.auth.models import User
from django.db import models

import pytest

from timeline_logger.handlers import (
    StructlogQueueHandler,
    TimelineLoggerHandler,
    _queue,
    _stop_listener,
    get_listener,
    timeline_handler_factory,
)
from timeline_logger.models import TimelineLog
from timeline_logger.typing import EventDetailsProtocol, EventDict


@dataclass
class EventDetails(EventDetailsProtocol):
    instance: models.Model
    extra_data: Mapping[str, object]

    def get_template_name(self) -> str:
        return "dummy.txt"

    def get_user(self) -> User | None:
        return None

    def get_extra_data(self) -> Mapping[str, object]:
        return self.extra_data


def assert_background_thread_not_running():
    assert get_listener() is None


@pytest.fixture(autouse=True)
def test_setup_and_teardown(request: pytest.FixtureRequest):
    # prevent connections from being closed for real, since tests run in a transaction
    # and require an open connection for further assertions
    use_real_close_conns = request.node.get_closest_marker("real_db_close")
    patch_context = (
        nullcontext()
        if use_real_close_conns
        else patch("timeline_logger.handlers.close_old_connections")
    )
    with patch_context:
        yield
    _stop_listener()


@pytest.fixture
def log_record() -> logging.LogRecord:
    return logging.LogRecord(
        name="timeline",
        level=logging.DEBUG,
        pathname=__file__,
        lineno=1,
        msg={"event": "dummy"},
        args=None,
        exc_info=None,
    )


@pytest.mark.parametrize(
    "use_queue,expected",
    [
        (False, TimelineLoggerHandler),
        (True, StructlogQueueHandler),
    ],
)
def test_build_expected_instance_based_on_setting(
    settings, use_queue: bool, expected: type[logging.Handler]
):
    settings.TIMELINE_HANDLER_USE_QUEUE = use_queue

    handler = timeline_handler_factory(adapter=lambda event_dict: None)

    assert isinstance(handler, expected)
    assert_background_thread_not_running()


@pytest.mark.django_db
def test_handler_flushes_immediately_in_non_queue_mode(
    admin_user: User, log_record: logging.LogRecord
):
    handler = TimelineLoggerHandler(
        adapter=lambda event_dict: EventDetails(
            instance=admin_user, extra_data=event_dict
        ),
        buffer_size=1000,
        flush_interval=999,
        use_queue_mode=False,
    )

    result = handler.handle(log_record)

    assert result is not False
    logs = TimelineLog.objects.for_object(admin_user)
    assert len(logs) == 1
    assert logs[0].template == "dummy.txt"
    assert logs[0].extra_data == {"event": "dummy"}


@pytest.mark.django_db
def test_handler_flushes_in_queue_mode_when_buffer_size_limit_reached(
    admin_user: User,
    log_record: logging.LogRecord,
    subtests: pytest.Subtests,
):
    handler = TimelineLoggerHandler(
        adapter=lambda event_dict: EventDetails(
            instance=admin_user, extra_data=event_dict
        ),
        buffer_size=2,
        flush_interval=999,
        use_queue_mode=True,
    )

    with subtests.test("buffer not yet full"):
        result = handler.handle(log_record)

        assert result is not False
        logs = TimelineLog.objects.for_object(admin_user)
        assert len(logs) == 0

    with subtests.test("buffer full"):
        result = handler.handle(log_record)

        assert result is not False
        logs = TimelineLog.objects.for_object(admin_user)
        assert len(logs) == 2


@pytest.mark.django_db
def test_handler_flushes_in_queue_mode_when_flush_interval_is_exceeded(
    admin_user: User,
    log_record: logging.LogRecord,
    subtests: pytest.Subtests,
):
    handler = TimelineLoggerHandler(
        adapter=lambda event_dict: EventDetails(
            instance=admin_user, extra_data=event_dict
        ),
        buffer_size=999,
        flush_interval=0.5,
        use_queue_mode=True,
    )

    with subtests.test("buffer not full, last write recent enough"):
        result = handler.handle(log_record)

        assert result is not False
        logs = TimelineLog.objects.for_object(admin_user)
        assert len(logs) == 0

    time.sleep(0.5)

    with subtests.test("buffer not full, last write too long ago"):
        result = handler.handle(log_record)

        assert result is not False
        logs = TimelineLog.objects.for_object(admin_user)
        assert len(logs) == 2


@pytest.mark.django_db
def test_closing_handler_flushes_the_queue(
    admin_user: User, log_record: logging.LogRecord
):
    handler = TimelineLoggerHandler(
        adapter=lambda event_dict: EventDetails(
            instance=admin_user, extra_data=event_dict
        ),
        buffer_size=999,
        flush_interval=999,
        use_queue_mode=True,
    )
    result = handler.handle(log_record)

    assert result is not False
    assert not TimelineLog.objects.exists()

    handler.close()

    assert TimelineLog.objects.count() == 1


@pytest.mark.django_db
def test_handler_adapter_can_return_None_when_nothing_needs_to_be_logged(
    log_record: logging.LogRecord,
):
    handler = TimelineLoggerHandler(
        adapter=lambda event_dict: None,
        buffer_size=999,
        flush_interval=999,
        use_queue_mode=False,
    )

    result = handler.handle(log_record)

    assert result is not False
    assert not TimelineLog.objects.exists()


@pytest.mark.django_db
def test_handler_can_be_disabled_with_setting(
    settings,
    admin_user: User,
    log_record: logging.LogRecord,
):
    settings.TIMELINE_HANDLER_DISABLED = True
    handler = TimelineLoggerHandler(
        adapter=lambda event_dict: EventDetails(
            instance=admin_user, extra_data=event_dict
        ),
        buffer_size=999,
        flush_interval=999,
        use_queue_mode=False,
    )

    result = handler.handle(log_record)

    assert result is not False
    assert not TimelineLog.objects.exists()


@pytest.mark.django_db
def test_handler_suppresses_unknown_errors(log_record: logging.LogRecord):
    def _raise(event_dict: EventDict):
        raise Exception("oof")

    handler = TimelineLoggerHandler(adapter=_raise, use_queue_mode=False)

    result = handler.handle(log_record)

    assert result is not False
    assert not TimelineLog.objects.exists()


@pytest.mark.real_db_close
@pytest.mark.django_db(transaction=True)
def test_integration_via_logging_dictconfig(
    settings,
    admin_user: User,
    monkeypatch: pytest.MonkeyPatch,
):
    settings.TIMELINE_HANDLER_USE_QUEUE = True
    monkeypatch.setenv("_TIMELINE_LOGGER_DEFER_LISTENER", "false")

    # set up a logger/handler only for this test to not break isolation/affect pytests
    # logging setup.
    logger_name = str(uuid.uuid4())
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                logger_name: {
                    "level": "DEBUG",
                    "()": "timeline_logger.handlers.timeline_handler_factory",
                    "adapter": lambda event_dict: EventDetails(
                        instance=admin_user, extra_data=event_dict
                    ),
                    "buffer_size": 1,  # force immediate flush
                    "flush_interval": 1,
                },
            },
            "loggers": {
                logger_name: {
                    "handlers": [logger_name],
                    "level": "DEBUG",
                    "propagate": False,
                }
            },
        }
    )
    logger = logging.getLogger(logger_name)
    assert get_listener() is not None

    logger.info({"event": "test-event"})

    _queue.join()

    assert TimelineLog.objects.count() == 1
    log_obj = TimelineLog.objects.get()
    assert log_obj.content_object == admin_user
    assert log_obj.extra_data == {"event": "test-event"}

"""
Provide robust and opinionated logging handlers.

`Log handlers <https://docs.python.org/3.12/library/logging.html#handler-objects>`_ are
responsible for sending the actual log records produced by loggers to their final
destination.

django-timeline-logger provides a handler that knows how to send log records from
structlog to the database and save them into the
:class:`timeline_logger.models.TimelineLog` model.

Our handler implementations take care of packages/modules that rely on process-forking
behaviour, notably:

* uwsgi
* celery workers with prefork pool
"""

from __future__ import annotations

import atexit
import logging
import os
import queue
import threading
import time
from collections.abc import Callable
from logging.handlers import QueueHandler, QueueListener
from typing import TYPE_CHECKING, Any

from django.db import close_old_connections
from django.utils.module_loading import import_string

from .conf import settings
from .typing import Adapter, EventDict, is_event_dict

if TYPE_CHECKING:
    from .models import TimelineLog

# public API
__all__ = ["TimelineLoggerHandler", "timeline_handler_factory"]

postfork: Callable[[Callable[..., Any]], Any]

# the uwsgi module is special - it's only available when the python code is loaded
# through uwsgi. With regular ``python`` usage, it does not exist.
try:  # pragma: no cover
    import uwsgi  # pyright: ignore[reportMissingModuleSource]
    from uwsgidecorators import postfork  # pyright: ignore[reportMissingModuleSource]
except ImportError:
    uwsgi = None
    postfork = lambda cb: None  # noqa: E731


logger = logging.getLogger(__name__)

_queue: queue.Queue = queue.Queue[EventDict](maxsize=0)
"""
Global queue singleton for the StructlogQueueHandler and QueueListener to communicate.

The queue is unbounded per the recommendations on an
`online article <https://runebook.dev/en/docs/python/library/logging.handlers/logging.handlers.QueueListener>`_.

TODO: it would probably be wise to monitor the queue size or when items get put on/taken
from the queue, e.g. with an OTel gauge instrument.
"""

_listener: QueueListener | None = None
"""
Queue listener singleton, ``None`` when it's not yet initialized.

Usually, the handler factory will result in the listener being initialized, but in
process-forking environments like uwsgi and celery workers, this is deferred until
after the process has forked. Failing to defer this results in deadlocks or other odd
behaviours.
"""

_lock = threading.Lock()
"""
Protect against race conditions between threads.

Trying to acquire a locked lock will block until it's unlocked (by another thread).

Note that Django's runserver runs in a subprocess, while typical production deployments
run multiple threads in one or more uwsgi/gunicorn processes.
"""


def get_listener() -> QueueListener | None:
    # Test helper to inspect the listener state.
    return _listener


def ensure_listener(*handlers: logging.Handler, _defer: bool) -> queue.Queue:
    """
    Ensure a listener thread is running for :class:`StructlogQueueHandler`.

    Creates a queue if it doesn't exist yet, and starts the background thread to
    listen to the queue to actually process the log records.

    We don't bother with preventing a background thread in the main runserver process
    that reloads the code and restarts the server - we don't expect any audit logs to
    be created there, and trying to detect these situations is too fragile compared
    to real uwsgi servers & management command situations. The idle background thread
    should not cause significant overhead.

    :arg _defer: Defer starting the background tread or not - by default on uwsgi we
      defer the startup and call te actual startup in te post fork hook.
    """
    global _listener, _queue

    def _ensure_listener(*args, **kwargs):
        return ensure_listener(*handlers, _defer=False)

    # we can't reliably use os.register_at_fork as it requires uwsgi's
    # py-call-uwsgi-fork-hooks flag, which can cause segfaults on Python 3.12:
    # https://github.com/unbit/uwsgi/issues/2738
    if _defer and uwsgi is not None:  # pragma: no cover
        postfork(_ensure_listener)

    # similar to uwsgi postfork, bind a handler when a celery worker process has
    # initialized
    try:  # pragma: no cover - no celery dependency available
        worker_process_init = import_string("celery.signals.worker_process_init")
        worker_process_init.connect(weak=False)(_ensure_listener)
    # Celery is an optional dependency
    except ImportError:
        pass

    # if a listener already exists, or if we must defer, short circuit and return the
    # queue already
    if _defer or _listener is not None:
        return _queue

    with _lock:
        _listener = QueueListener(_queue, *handlers, respect_handler_level=True)
        _listener.start()
        atexit.register(_stop_listener)
        return _queue


def _stop_listener():
    """
    Shut down (and drain) the listener thread/queue.
    """
    global _listener

    with _lock:
        if _listener is None:
            return
        try:
            _listener.stop()  # drains the queue before stopping
        finally:
            _listener = None


class StructlogQueueHandler(QueueHandler):
    """
    Keep structlog log.record dict as a dict.

    The stdlib implementation by default formats the log record to a string and clears
    most attributes to make them pickleable.
    """

    def prepare(self, record: logging.LogRecord):
        assert is_event_dict(record.msg), "Only structlog event dicts are expected"
        return record


class TimelineLoggerHandler(logging.Handler):
    """
    Save a log record into a django-timeline-logger record.

    Logs saved to the local database are typically intended to be easily accessible,
    e.g. audit logs, without requiring access to a dedicated log storage like Loki.

    This handler goes hand-in-hand with structlog:

    * it looks at the structlog event to call additional (pre)-processing, allowing
      additional metadata extraction
    * the additional log attributes are stored as structured data

    The handler keeps an internal buffer to optimize log record insert. The drawback of
    this is that there may be substantial lag for some log records to be written to the
    database, as either new log records need to arrive or the handler shutdown needs to
    be triggered to force another flush. If this is not acceptable, set the buffer size
    to 1 to force instant flushes.

    :arg adapter: The adapter function that takes a structlog event dict and converts
      it into something that speaks :class:`timeline_logger.typing.EventDetailsProtocol`
      understood by the timeline logger handler.
    :arg use_queue_mode: Marker for queue/direct mode. In direct mode, the buffer size
      is capped at ``1`` and old database connections are not closed.
    :arg buffer_size: Maximum size for the internal buffer. Once the number of log
      records is equal to or exceeds this, they will be written to the database. Until
      that time the records only exist in memory.
    :arg flush_interval: Maximum age between database writes. If the buffer is not full
      yet, but ``flush_interval`` has elapsed since the last write, flush the buffer
      anyway.
    """

    buffer: list[TimelineLog]

    def __init__(
        self,
        *,
        adapter: Adapter,
        use_queue_mode: bool = False,
        buffer_size: int = 5,
        flush_interval: float = 3.0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.adapter = adapter

        # store configuration options
        self.use_queue_mode = use_queue_mode
        self.buffer_size = buffer_size if use_queue_mode else 1
        self.flush_interval = flush_interval

        # track internal buffer state
        self.buffer = []
        self._last_flush = time.monotonic()

    def emit(self, record: logging.LogRecord):
        try:
            self._emit_to_db(record)
        except Exception as exc:
            self.handleError(record)

            # XXX: should we add explicit transaction savepoint so we can recover when
            # running in the main thread?
            logger.error("log_saving_failed", exc_info=exc)
            if on_error := settings.TIMELINE_HANDLER_ON_ERROR:
                on_error(exc)

    def _emit_to_db(self, record: logging.LogRecord):
        from .models import TimelineLog

        if settings.TIMELINE_HANDLER_DISABLED:
            return

        assert is_event_dict(record.msg), "Only structlog event dicts are expected"

        self._maybe_close_old_connections()
        event_details = self.adapter(record.msg)
        if event_details is None:
            return

        # create DB record
        # TODO: validate that the provided template name exists!
        self.buffer.append(
            TimelineLog(
                content_object=event_details.instance,
                template=event_details.get_template_name(),
                extra_data=event_details.get_extra_data(),
                user=event_details.get_user(),
            )
        )

        # check if we need to flush the buffer
        now = time.monotonic()
        if (
            len(self.buffer) >= self.buffer_size
            or (now - self._last_flush) > self.flush_interval
        ):
            self._flush()

    def _flush(self):
        """
        Flush the buffer to the database.
        """
        from .models import TimelineLog

        TimelineLog.objects.bulk_create(self.buffer)
        self.buffer = []
        self._last_flush = time.monotonic()
        self._maybe_close_old_connections()

    def _maybe_close_old_connections(self) -> None:
        # when running in a separate thread, clean up old connections. Because the
        # connection lives in its own thread, it doesn't get cleaned up by django's
        # 'request_finished' signal, so we must manually schedule the cleanup. Django
        # will re-open the connection when queries are made.
        if self.use_queue_mode:
            close_old_connections()

    def close(self):
        try:
            self._flush()
        finally:
            self._maybe_close_old_connections()
            super().close()


def timeline_handler_factory(
    *, adapter: Adapter, buffer_size: int = 5, flush_interval: float = 3.0
) -> StructlogQueueHandler | TimelineLoggerHandler:
    """
    Create a logging handler instance suitable for production or testing.

    By default, a queue-based handler is configured so that the actual logging of
    messages can be offloaded to a worker thread. This improves performance by taking
    database queries out of the main thread, and improves log integrity because the
    log insertions run in a separate thread and associated database transaction.

    However, in (unit) test setups, you want to force the logs to be written in the same
    test transaction so that at the end of the test, the log record creation is rolled
    back by the test transaction, otherwise you break test isolation substantially
    and/or slow down test suites considerably by forcing them to be
    :class:`django.test.TransactionTestCase`.

    The appropriate handler is selected based on the ``TIMELINE_HANDLER_USE_QUEUE``
    Django setting.

    Note that you cannot change this setup at runtime in tests through
    :func:`django.test.override_settings`, as the logging config does not get
    reinitialized when settings change (as it should be!). You should configure CI/local
    test environments to apply conditional configurations.

    :arg adapter: The adapter function that takes a structlog event dict and converts
      it into something that speaks :class:`timeline_logger.typing.EventDetailsProtocol`
      understood by the timeline log handler.
    :arg buffer_size: Maximum size for the internal buffer. Passed along to the
      :class:`TimelineLoggerHandler` initializer.
    :arg flush_interval: Maximum age between database writes. Passed along to the
      :class:`TimelineLoggerHandler` initializer.
    """
    use_queue: bool = settings.TIMELINE_HANDLER_USE_QUEUE
    timeline_logger_handler = TimelineLoggerHandler(
        adapter=adapter,
        use_queue_mode=use_queue,
        buffer_size=buffer_size,
        flush_interval=flush_interval,
    )

    # if the project does not opt out of the queue, return the handler as-is which will
    # run in the main thread
    if not use_queue:
        return timeline_logger_handler

    # otherwise set up the queue system. First, check if we explicitly opt-out of
    # deferred queue listener start.
    _defer: bool
    # Using an environment variable is the most robust way to defer in celery workers.
    match os.environ.get("_TIMELINE_LOGGER_DEFER_LISTENER", "").lower():
        case "false" | "0":
            _defer = False
        case "true" | "1":
            _defer = True
        case _:  # pragma: no cover
            _defer = uwsgi is not None

    queue = ensure_listener(timeline_logger_handler, _defer=_defer)
    return StructlogQueueHandler(queue=queue)

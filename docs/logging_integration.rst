.. _stdlib_logging_integration:

==========================
Stdlib logging integration
==========================

Python has a standard library `logging <https://docs.python.org/3.12/library/logging.html>`_
module that's commonly used in projects and external packages.

`Structlog <https://www.structlog.org/en/stable/index.html>`_ builds on top of this and
adds structure to your log messages/events.

Django-timeline-logger brings these worlds together - it supports saving log records
created through structlog into the database (to the :class:`timeline_logger.models.TimelineLog`
model), and it does this by configuring the standard library logging mechanisms.

.. warning:: The log message (``logging.LogRecord.msg``) must be a dictionary -
   string-based log messages are not supported.

Configuration
=============

**Settings**

To use the integration, you must define a handler in the Django ``LOGGING``
configuration, and direct logs from your logger(s) to this handler. For example:

.. code-block:: python
    :linenos:
    :emphasize-lines: 3, 27-33, 38

    import structlog

    from my_project.logging import adapter

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
                "foreign_pre_chain": [
                    structlog.contextvars.merge_contextvars,
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                ],
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
            "timeline_logger": {
                "level": "DEBUG",
                "()": "timeline_logger.handlers.timeline_handler_factory",
                "adapter": adapter,  # see below for example
                "buffer_size": 15,
                "flush_interval": 15.0,  # in seconds
            },
        },
        "loggers": {
            "audit": {
                # log both stdout/stderr and the database
                "handlers": ["console", "timeline_logger"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

**Adapter callback**

The adapter callback is a function that takes a structlog
:class:`timeline_logger.typing.EventDict` and transforms it into an object that carries
the database model details. For example:

.. code-block:: python

    from structlog.typing import EventDict
    from timeline_logger.typing import EventDetailsProtocol


    @dataclass
    class EventDetails(EventDetailsProtocol):
        instance: models.Model
        user: User | None
        extra_data: Mapping[str, object]

        def get_template_name(self) -> str:
            return "timeline_logger/default.txt"

        def get_user(self) -> User | None:
            return self.user

        def get_extra_data(self) -> Mapping[str, object]:
            return self.extra_data


    def adapter(event_dict: EventDict) -> EventDetails | None:
        from django.contrib.auth.models import User

        assert "event" in event_dict

        match event_dict:
            case {
                "event": "user_viewed_pii" as event,
                "user": str(viewer_username),
                "subject": str(subject_username),
            }:
                subject = User.objects.get(username=subject_username)
                viewer = User.objects.get(username=viewer_username)
                return EventDetails(
                    instance=subject,
                    user=viewer,
                    extra_data={"event": event},
                )
            case _:
                return None

**Usage**

You can then use your logger as usual:

.. code-block:: python

    import structlog

    audit_logger = structlog.stdlib.get_logger("audit")

    audit_logger.info(
        "user_viewed_pii",
        user=request.user.username,
        subject=subject.username,
    )

and the events will be written to the database.

How it works
============

When django initializes, it sets up logging. Typically this results in
``logging.config.dictConfig`` being called with your Django ``LOGGING`` setting.

This leads to ``timeline_handler_factory`` being called, which initializes and
configures the appropriate handler. In queue mode (enabled by default), a background
thread will start that reads from a queue. The ``StructlogQueueHandler`` is configured
with this queue, and any log event that arrives is offloaded to the worker thread.

``TimelineLoggerHandler`` runs in the worker thread and continuously reads from the
queue. When a log event arrives, it is passed to the configured ``adapter`` callback.
This adapter is responsible for transforming the log event into something
``TimelineLog`` understands - or ``None`` to skip saving it entirely.

The resulting ``TimelineLog`` instance is added to an internal buffer. The buffer is
written to the database once enough items have arrived or the configured flush interval
has elapsed.

Because the writes happen in a worker thread, these use a separate database transaction,
and you can never lose log records because of rolled back transactions in the main
thread.

Testing
=======

Set:

.. code-block:: python

    TIMELINE_HANDLER_USE_QUEUE = False

when running your Django test suite. It will skip the thread and queue for log messages,
and synchronously insert the log events in the database. This will all happen in the
same database transaction that your test is currently running in, so at the end of the
test when the transaction is rolled back, your log events are rolled back too. This
prevents broken isolation between tests.

If, for some reason, you need to enable the thread-based logging, you should use a
``TransactionTestCase``, but be warned - these are much slower.

.. note:: This setting is global and cannot be changed on an individual test-basis,
   because Django only configures logging once when it initializes.

Third-party packages support
============================

Many third party packages should work out of the box. However, you will probably
encounter issues like deadlocks on tools that make use of process forking
(``os.fork()``), because we start a background thread for the log handling.

Packages known to be problematic and their support + specific instructions are
documented here.

uWSGI
-----

uWSGI forks worker processes. We handle uwsgi already out of the box by detecting
whether we're running in a uwsgi context or not. The background threads are started
only after the master process has forked.

Using the ``--lazy-apps`` options may also avoid the issue in the first place.

Celery worker
-------------

Celery workers by default use a process pool, where worker processes are spawned by the
main process. When starting Celery worker in prefork mode, make sure that you set the
environment variable:

.. code-block:: sh

    _TIMELINE_LOGGER_DEFER_LISTENER=true celery --app myapp worker

We listen and wait for the ``worker_process_init`` signal to start the background
thread.

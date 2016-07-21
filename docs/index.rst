.. Django Timeline Logger documentation master file, created by
   sphinx-quickstart on Thu Jun 30 17:07:28 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================
Django Timeline Logger's documentation
======================================

.. rubric:: A reusable Django app to log actions and display them in a timeline.

.. image:: https://travis-ci.org/maykinmedia/django-timeline-logger.png
    :target: https://travis-ci.org/maykinmedia/django-timeline-logger

.. image:: https://codecov.io/gh/maykinmedia/django-timeline-logger/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/django-timeline-logger

.. image:: https://badge.fury.io/py/django-timeline-logger.svg
    :target: https://badge.fury.io/py/django-timeline-logger


Overview
========

Django Timeline Logger is a simple pluggable application that adds events
logging and reporting to your Django projects.

It easily enables you to generate customized log messages on events, thus
providing your backend with a logging system slightly more advanced and
customizable than the builtin "admin logs" generated via ``LogEntry``.


Requirements
============

Django Timeline Logger makes use of Django's ``contrib.postgres.JSONField``,
then your backend will need:

   - At least Django-1.9_.
   - At least PostgreSQL-9.4_.
   - At least psycopg2-2.5.4_.


Contents
========

.. toctree::
   :maxdepth: 2

   installation
   usage
   sending_log_reports
   settings
   contributing


License
=======

Licensed under the `MIT License`_.


Source Code and contributing
============================

The source code can be found on Github_.

Bugs can also be reported on the Github_ repository, and pull requests
are welcome. See :ref:`contributing` for more details.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Django-1.9: https://docs.djangoproject.com/en/1.9/releases/1.9/
.. _PostgreSQL-9.4: https://www.postgresql.org/docs/9.4/static/release-9-4.html
.. _psycopg2-2.5.4: https://pypi.python.org/pypi/psycopg2/2.5.4
.. _MIT License: https://opensource.org/licenses/MIT
.. _Github: https://github.com/maykinmedia/django-timeline-logger

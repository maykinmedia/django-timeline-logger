.. Django Timeline Logger documentation master file, created by
   sphinx-quickstart on Thu Jun 30 17:07:28 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================
Django Timeline Logger's documentation
======================================

.. rubric:: A reusable Django app to log actions and display them in a timeline.

|build-status| |code-quality| |coverage| |black|

|python-versions| |django-versions| |pypi-version|


Overview
========

Django Timeline Logger is a simple pluggable application that adds events
logging and reporting to your Django projects.

It easily enables you to generate customized log messages on events, thus
providing your backend with a logging system slightly more advanced and
customizable than the builtin "admin logs" generated via ``LogEntry``.


Requirements
============

Django Timeline Logger makes use of Django's ``django.db.models.JSONField``,
then your backend will need:

   - One of the maintained Django_ versions
   - A database backend with support for the JSONField_ for your Django version

Contents
========

.. toctree::
   :maxdepth: 2

   installation
   usage
   sending_log_reports
   settings
   contributing
   changelog


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


.. _Django: https://www.djangoproject.com/download/
.. _JSONField: https://docs.djangoproject.com/en/dev/ref/models/fields/#jsonfield
.. _MIT License: https://opensource.org/licenses/MIT
.. _Github: https://github.com/maykinmedia/django-timeline-logger

.. |build-status| image:: https://github.com/maykinmedia/django-timeline-logger/actions/workflows/ci.yml/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/django-timeline-logger/actions/workflows/ci.yml

.. |code-quality| image:: https://github.com/maykinmedia/django-timeline-logger/actions//workflows/code_quality.yml/badge.svg
    :alt: Code quality checks
    :target: https://github.com/maykinmedia/django-timeline-logger/actions//workflows/code_quality.yml

.. |coverage| image:: https://codecov.io/gh/maykinmedia/django-timeline-logger/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/django-timeline-logger
    :alt: Coverage status

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-timeline-logger.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-timeline-logger.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-timeline-logger.svg
    :target: https://pypi.org/project/django-timeline-logger/

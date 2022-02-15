======================
django-timeline-logger
======================

A reusable Django app to log actions and display them in a timeline

|build-status| |code-quality| |coverage| |black|

|python-versions| |django-versions| |pypi-version|

Prerequisites
=============

This project uses ``django.contrib.postgres.JSONField``, and as such, you need:

* at least Django 2.2+
* at least PostgreSQL 10
* at least psycopg2 2.5.4
* A modern setuptools version


Installation
============

Install from PyPI by running

    pip install django-timeline-logger

Add ``'timeline_logger'`` to your ``INSTALLED_APPS``.

Run the migrations:

    python manage.py migrate


Usage in templates
==================

A custom template tag is provided to render the message of a log entry, for example::

    {% extends "timeline_logger/base.html" %}
    {% load timeline %}

    {% block timeline %}
        <ul class="timeline__list col__22--vw">
        {% for log in object_list %}
            <li class="timeline__entry">
                {% render_message log in_view=True %}
            </li>
        {% endfor %}
        </ul>
    {% endblock timeline %}


This way, you can pass extra context to the template used for the log object.


Documentation
=============

The extended documentation is available on `Read the Docs`_.

.. _Read the Docs: http://django-timeline-logger.readthedocs.io/en/latest/


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

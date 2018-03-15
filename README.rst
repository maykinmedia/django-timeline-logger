======================
django-timeline-logger
======================

A reusable Django app to log actions and display them in a timeline

.. image:: https://travis-ci.org/maykinmedia/django-timeline-logger.svg?branch=master
    :target: https://travis-ci.org/maykinmedia/django-timeline-logger

.. image:: https://codecov.io/gh/maykinmedia/django-timeline-logger/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/django-timeline-logger

.. image:: https://badge.fury.io/py/django-timeline-logger.svg
    :target: https://badge.fury.io/py/django-timeline-logger


Prerequisites
=============

This project uses `django.contrib.postgres.JSONField`, and as such, you need:

* at least Django 1.11
* at least PostgreSQL 9.4
* at least psycopg2 2.5.4


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

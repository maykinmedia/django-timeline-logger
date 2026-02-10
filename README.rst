======================
django-timeline-logger
======================

A reusable Django app to log actions and display them in a timeline

|build-status| |code-quality| |ruff| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

Prerequisites
=============

This project uses ``django.db.models.JSONField``, and as such, you need:

* Django 4.2+
* a database supporting ``django.db.models.JSONField``

Installation
============

Install from PyPI by running

    pip install django-timeline-logger

Add ``'timeline_logger'`` to your ``INSTALLED_APPS``.

Run the migrations:

    python manage.py migrate


Usage in templates
==================

A custom template tag is provided to render the message of a log entry, for example:

.. code-block:: django

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

Local development
=================

To install and develop the library locally, use:

.. code-block:: bash

    pip install -e .[tests,docs,release]

When running management commands via ``django-admin``, make sure to add the root
directory to the python path (or use ``python -m django <command>``):

.. code-block:: bash

    export PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings_pg
    django-admin check
    # or other commands like:
    # django-admin makemessages -l nl


.. |build-status| image:: https://github.com/maykinmedia/django-timeline-logger/actions/workflows/ci.yml/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/django-timeline-logger/actions/workflows/ci.yml

.. |code-quality| image:: https://github.com/maykinmedia/django-timeline-logger/actions/workflows/code_quality.yml/badge.svg
    :alt: Code quality checks
    :target: https://github.com/maykinmedia/django-timeline-logger/actions/workflows/code_quality.yml

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |coverage| image:: https://codecov.io/github/maykinmedia/django-timeline-logger/graph/badge.svg?token=ey3tios7Sn
    :target: https://codecov.io/github/maykinmedia/django-timeline-logger
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/django-timeline-logger/badge/?version=latest
    :target: https://django-timeline-logger.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-timeline-logger.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-timeline-logger.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-timeline-logger.svg
    :target: https://pypi.org/project/django-timeline-logger/

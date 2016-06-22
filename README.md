# django-timeline-logger
A reusable Django app to log actions and display them in a timeline


## Prerequisites

This project uses `django.contrib.postgres.JSONField`, and as such, you need:

* at least Django 1.9
* at least PostgreSQL 9.4
* at least psycopg2 2.5.4


## Installation

Install from PyPI by running

    pip install django-timeline-logger

Add `'timeline_logger'` to your `INSTALLED_APPS`.

Run the migrations:

    python manage.py migrate

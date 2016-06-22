# django-timeline-logger
A reusable Django app to log actions and display them in a timeline


[![Build Status](https://travis-ci.org/maykinmedia/django-timeline-logger.svg?branch=master)](https://travis-ci.org/maykinmedia/django-timeline-logger)
[![codecov](https://codecov.io/gh/maykinmedia/django-timeline-logger/branch/develop/graph/badge.svg)](https://codecov.io/gh/maykinmedia/django-timeline-logger)
[![Coverage Status](https://coveralls.io/repos/github/maykinmedia/django-timeline-logger/badge.svg?branch=master)](https://coveralls.io/github/maykinmedia/django-timeline-logger?branch=master)
[![PyPI version](https://badge.fury.io/py/django-timeline-logger.svg)](https://badge.fury.io/py/django-timeline-logger)


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

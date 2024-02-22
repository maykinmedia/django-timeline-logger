=========
Changelog
=========

4.0.0 (2024-02-22)
==================

No changes in functionality or public API, just our supported versions of Python/Django.

* Dropped Python < 3.10 support
* Confirmed support for Python 3.12 (Removed usage of ``pkg_resources``)
* Dropped support for Django 4.1
* Update tooling and move to ``pyproject.toml``


3.0.0 (2023-07-11)
==================

No changes in functionality or public API, just our supported versions of Python/Django.

* Dropped Python < 3.8 support
* Confirmed support for Python 3.11
* Dropped support for end-of-life Django 2.x, 4.0.x
* Confirmed support for Django 4.2

2.1.0 (2022-04-13)
==================

* Dropped support for end-of-life Django 2.2.x
* Confirmed support for Django 4.0
* Swapped to Django's generic ``models.JSONField``, adding support for databases other
  than PostgreSQL
* Changed primary key field to ``BigIntegerField`` for the ``TimelineLog`` model
* Added database indices to speed up ``TimelineLog`` read operations

2.0.0 (2022-02-15)
==================

No changes in functionality or public API, just our supported versions of Python/Django.

* Dropped Python 2, Python < 3.6 support
* Dropped Django 1.11, 2.0 and 2.1 support
* Added explicit support for Django 2.2 and 3.2
* Added explicit support for Python 3.6, 3.7, 3.8, 3.9 and 3.10

1.1.2 (2018-05-30)
==================

Fixed packaging mistake - Dutch translations are now included.

1.1.1 (2018-05-04)
==================

Added Dutch translations (PR#14, thanks @josvromans)

1.1 (2018-04-17)
================

* Added django-import-export support

* Added a demo project to showcase the usage/integrations.

1.0 (2018-03-15)
================

Breaking changes
----------------

* Changed the GFK object_id field to a text field, so that non-integer primary
  keys are supported. This may come at a (small) performance hit. Depending
  on the data you're storing, the backwards migration may break.

* Dropped Django 1.10 support, per Django's version support policy. If you're
  still on Django 1.10, you should upgrade, but other than that the app
  probably still works.

New features
------------

* You can now create log entries without referring to a specific object
  (thanks @tsiaGeorge).

* Support non-integer PKs for objects (see #7, thanks for the feedback @holms)

Other
-----

* first pass at better supporting internationalization

* cleaned up package a bit, added isort etc.

Pre 1.0
=======

Best guess is looking at the git log, sorry.

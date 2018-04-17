=========
Changelog
=========

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

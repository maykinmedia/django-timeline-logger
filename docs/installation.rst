============
Installation
============

To install Django Timeline Logger you can use PyPI:

.. code-block:: sh

   pip install django-timeline-logger

Once installation is complete, you can enable the application in your Django
project by adding it to ``INSTALLED_APPS`` in the regular way:

.. code-block:: python

   INSTALLED_APPS = [
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       ...

       'timeline_logger',
   ]

Then, run the migrations:

.. code-block:: sh

   python manage.py migrate timeline_logger

and configure your `urls.py` as you desire, e.g.

.. code-block:: python

    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("timeline/", include("timeline_logger.urls")),
    ]

You can now start using the application. Go to :ref:`usage` section for the
details.

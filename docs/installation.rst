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

You can now start using the application. Go to :ref:`usage` section for the
details.

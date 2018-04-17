.. _usage:

=====
Usage
=====

Django Timeline Logger works by using a custom model ``TimelineLog``, which is
designed to store:

    - A Django model instance (a database object).
    - A timestamp.
    - A user instance (optional).
    - A path to a template (optional, defaults to ``timeline_logger/default.txt``).
    - A context (optional).

Given those details, it's pretty clear how it works: whenever you want to log
an event in your system, you create a ``TimelineLog`` for it, passing the data
you consider useful in the context and using a template to render the message.

The context is stored in a ``django.contrib.postgres.JSONField``, which basically
accepts a Python dictionary representing JSON data, to be built by you with the
data you want to pass to the message template.


Default example
===============

An example of a default usage of the ``TimelineLog`` model could be as follows.
Imagine you have a "blog" application where your users can create posts,
stored by using a Django model ``Post``.

Using the default behaviour of ``TimelineLog``, you can create a log each time
a user posts a new entry in the blog, like this:

.. code-block:: python

   from timeline_logger.models import TimelineLog


   # Whatever logic you have before creating the post entry.
   ...

   post = Post.objects.create(
       title='New blog entry',
       body=post_text
   )

   log = TimelineLog.objects.create(
       content_object=post,
       user=my_user
   )

There you go. A new timeline entry has been created to record the event that
a user posted a new blog entry.

You can then see the default message for such event by calling the 
``TimelineLog.get_message()`` method:

.. code-block:: python

   log.get_message()

That function will return a text string, like this one:

``'July 1, 2016, 9:08 a.m. - Anonymous user event on New blog entry\n'``

With all this in place, you can now access the view included with the Django
Timeline Logger package: http://localhost:8000/timeline to see a paginated
list of your event logs.


Custom messages using templates and context
===========================================

Of course, you want to have your own custom messages for each different event
you want to track, maybe showing in the log as more data as possible. You can
easily do that by using regular Django templates in your ``TimelineLog`` instances.

Let's see an example of usage. Imagine you have a web shop and you want to log
user purchases of certain items, whatever the item is. In this scenario, you
could have a view to handle a user form submission representing a purchase. You
should be able to log each purchase with any details you want by doing something
like this:

.. code-block:: python

   from django.views.generic import CreateView

   from timeline_logger.models import TimelineLog

   from my_app.models import Invoice, Item


   class PurchaseView(CreateView):
       """ Manages a client purchase and creates the invoice """
       model = Invoice
       ...

       def post(self, request, *args, **kwargs):
           response = super(PurchaseView, self).post(request, *args, **kwargs)

           # The sold item.
           item = Item.objects.get(pk=kwargs['item'])

           # Add some extra data to the log message.
           extra_data = {'invoice': self.object}

           # Log the purchase event.
           TimelineLog.objects.create(
               content_object=item,
               user=request.user,
               template='timeline_logger/purchase.txt',
               extra_data=**extra_data
           )

           return response

You logged there the "purchase event", passing the ``request`` object, using a
custom template to render your own message and some context for it. A simple
template you can write in your ``my_app/templates/timeline_logger`` directory
could look like this:

.. code-block:: django

   {% load i18n %}
   {% blocktrans trimmed with timestamp=log.timestamp user=log.user|default:_('Anonymous user') object=log.content_object extra=log.exta_data|safe %}
      {{ timestamp }} - {{ user }} purchased item "{{ object }}", using payment method "{{ extra.invoice.method }}", for a total price of {{ extra.invoice.total }} €.
   {% endblocktrans %}

So, in your http://localhost:8000/timeline view, this log entry will appear more
or less as follows:

   July 4, 2016, 8:13 a.m. - John Doe purchased item "Nescafé Dolce Gusto", using payment method "PayPal", for a total price of 35 €.


Log from requests
=================

Probably you'll better like to log events based on user requests, like for
example a user comment in a blog post, a form submission, a click in a "like" 
button or a purchase in your web shop.

You can easily do so by using the ``TimelineLog.log_from_request`` method,
which accepts a Django ``HTTPRequest`` object (accessible in all Django views 
via the ``request`` parameter or the ``self.request`` view class attribute) and
a Django model instance, plus an optional template and its context.

In our previous example, we can substitute the ``TimelineLog.objects.create(...``
part by this:

.. code-block:: python

   TimelineLog.log_from_request(
       request,
       item,
       'timeline_logger/purchase.txt',
       **extra_data
   )

And the resulting log instance and message will be the same.

Django-import-export integration
================================

Django-timeline-logger ships with a ``ModelResource``:

.. code-block:: python

    from timeline_logger.resources import TimelineLogResource

    ...

 It's not enabled in the default admin, as django-import-export is an
 optional dependency.

===================
Sending log reports
===================

Timeline Logger includes a Django management command that you can add to a
cronjob, or trigger manually when you want, to send reports via email about
your site usage to those people you want.


Report mailing
==============

The management command can be called like this in "default" mode:

.. code-block:: sh

    python manage.py report_mailing

In this mode, **only** those Django system users marked as "staff" member **and**
"superuser" will be notified via email. You can change this default behaviour
by using some command arguments and Django project :ref:`settings`.


Options
-------

The command options are:

   - ``--all``: Send notification emails to **all** users registered in the
     system.
   - ``--staff``: Send notification emails **only** to the system users
     marked as ``is_staff=True``.
   - ``--recipients_from_setting``: Send notification emails to those email
     addresses listed in ``TIMELINE_DIGEST_EMAIL_RECIPIENTS`` setting.


Custom email notifications
--------------------------

In case you don't like the default look and feel of the HTML notification email,
you can design your own template and place it in your project 
``templates/timeline_logger/`` directory using the name ``notifications.html``.

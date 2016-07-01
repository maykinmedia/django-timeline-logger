========
Settings
========

Timeline Logger default behaviour can also be customized by using the next
application settings in your project:

   - ``TIMELINE_DEFAULT_TEMPLATE``: defines the Django template used for the 
     standard  logs message. Defaults to ``timeline_logger/default.txt``.
   - ``TIMELINE_DIGEST_EMAIL_RECIPIENTS``: defines a fixed list of email addresses
     that must be notified when running the ``report_mailing`` command, without
     any else being notified at all. Could be system registered users or not.
     Defaults to ``None``.
   - ``TIMELINE_DIGEST_EMAIL_SUBJECT``: a string defining a subject for the 
     notification email. Defaults to "Events timeline".
   - ``TIMELINE_DIGEST_FROM_EMAIL``: the "sender" email that will be used to
     send the notifications. Defaults to ``None``, and then if it's not set it
     will use Django's ``DEFAULT_FROM_EMAIL`` setting "webmaster@localhost".
   - ``TIMELINE_PAGINATE_BY``: the number of log entries that will be shown for
     each page in your http://localhost:8000/timeline view. Defaults to 25.
   - ``TIMELINE_USER_EMAIL_FIELD``: in case you are using a custom Django 
     ``User`` model with the user email stored in a specific field, it allows
     you to specify such field. Defaults to ``'email'``.

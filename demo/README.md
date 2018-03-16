# Demo project for Django Timeline Logger

## Getting started

Navigate to the demo project:

    cd demo

### Dependencies

In your (virtual) environment, make sure you have pip-tools:

    pip install pip-tools

Next, compile the dependencies:

    pip-compile

And install the dependencies:

    pip install -r requirements.txt

### Database

Since only PostgreSQL is supported, make sure postgres is running.

You can use the following environment variables to control the database
configuration:

* `PGDATABASE`
* `PGUSER`
* `PGPASSWORD`
* `PGHOST`
* `PGPORT`

See the `settings.py` file for the defaults.

Create the database before running migrate:

    createdb timeline_logger -O postgres -U postgres -p 5432

and migrate:

    ./manage.py migrate

Next, you can load the demo data:

    ./manage.py loaddata demo.json

This installs a superuser object with credentials: `timeline-logger` / `timeline-logger`.

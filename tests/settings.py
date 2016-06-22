SECRET_KEY = 'Timeline logger'

DATABASES = {
    'default': {
        # Memory resident database, for easy testing.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'timeline_logger',
    'tests'
]

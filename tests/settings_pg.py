from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'timeline_logger',
        'USERNAME': 'postgres',
        'PASSWORD': '',
    }
}

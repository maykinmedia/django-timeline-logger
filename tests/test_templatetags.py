import pytest
from django.conf import settings
from django.template.loader import render_to_string

from .compat import patch
from .factories import TimelineLogFactory


@pytest.mark.skipif(
    settings.DATABASES['default']['ENGINE'] != 'django.db.backends.postgresql',
    reason='Requires PostgreSQL'
)
@pytest.mark.django_db
def test_render_message():
    log = TimelineLogFactory.create(extra_data={'foo': 'bar'})
    with patch.object(log, 'get_message') as mock_get_message:
        render_to_string('test_render_message', {'log': log})
    mock_get_message.assert_called_once_with(template=None, extra_context='yes')

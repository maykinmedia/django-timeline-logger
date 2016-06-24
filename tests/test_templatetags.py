from unittest import mock

import pytest

from django.template.loader import render_to_string

from .factories import TimelineLogFactory


@pytest.mark.django_db
def test_render_message():
    log = TimelineLogFactory.create(extra_data={'foo': 'bar'})
    with mock.patch.object(log, 'get_message') as mock_get_message:
        render_to_string('test_render_message', {'log': log})
    mock_get_message.assert_called_once_with(template=None, extra_context='yes')

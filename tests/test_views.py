try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

import pytest

from .factories import TimelineLogFactory


@pytest.mark.django_db
def test_listview(client):
    log_entries = TimelineLogFactory.create_batch(26)
    response = client.get(reverse("timeline:timeline"))
    assert response.status_code == 200
    queryset = response.context["object_list"]
    assert queryset.count(), 25
    assert log_entries[0] not in queryset, "Oldest object should not be displayed"
    assert log_entries[-1] in queryset, "Newest log entry should be displayed"

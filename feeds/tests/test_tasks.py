from datetime import timedelta
from unittest import mock

import pytest
from django.utils import timezone
from feeds.tasks import feed_updater


@pytest.mark.django_db
@mock.patch("feeds.helpers.request_feed")
@mock.patch("feeds.tasks.BaseTask.on_success")
@mock.patch("django.core.cache.cache")
def test_success(mocked_cache, mocked_on_success, request_feed, feed):
    feed_updater(feed.id)
    assert request_feed.called_once_with(feed.url)
    assert mocked_on_success.called_once()

    key = f"{feed.uuid.hex}_update_state_{feed.user_id}"
    value = "SUCCESS"
    assert mocked_cache.called_once_with(key, value)

    feed.refresh_from_db()
    assert feed.is_active
    assert feed.items.count() > 0
    assert feed.last_updated <= timezone.now() - timedelta(milliseconds=1)

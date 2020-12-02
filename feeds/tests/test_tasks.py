from datetime import timedelta
from unittest import mock

import pytest
from django.utils import timezone
from feeds.tasks import feed_updater


@pytest.mark.django_db
@mock.patch("feeds.helpers.request_feed")
@mock.patch("feeds.tasks.BaseTask.on_success")
@mock.patch("django.core.cache.cache.set")
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


@pytest.mark.django_db
@mock.patch("feeds.tasks.request_feed")
@mock.patch("feeds.tasks.BaseTask.on_failure")
@mock.patch("feeds.tasks.BaseTask.on_retry")
@mock.patch("django.core.cache.cache.set")
def test_failure(
    mocked_cache,
    mocked_on_retry,
    mocked_on_failure,
    request_feed,
    feed,
):

    request_feed.side_effect = error = Exception()

    with pytest.raises(Exception):
        feed.url = "http://fake.com"
        feed.save()
        feed_updater(feed.id)
    assert mocked_on_retry.called_with(exc=error)
    assert request_feed.called_with(feed.url)
    assert mocked_on_failure.called_once()

    feed.refresh_from_db()
    assert not feed.is_active

    key = f"{feed.uuid.hex}_update_state_{feed.user_id}"
    value = "RETRYING-http://fake.com is not a valid rss feed"
    assert mocked_cache.called_with(key, value)

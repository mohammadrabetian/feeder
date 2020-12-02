from unittest import mock

import pytest
from django.utils import timezone
from faker import Faker

from .queries import (
    delete_feed,
    feed_item_query,
    feed_query,
    feed_update_state,
    follow_feed,
    read_item,
    register_feed,
    unfollow_feed,
    unread_item,
    update_feed,
)

fake = Faker()


@pytest.mark.django_db
def test_register_feed(graphql_request, user):
    response = graphql_request(
        graphql_request_data={
            "query": register_feed,
            "user": user,
            "variables": {"url": fake.url()},
        }
    )
    assert response["data"]["registerFeed"]["feed"]["uuid"]
    assert "errors" not in response


@pytest.mark.django_db
@mock.patch("feeds.models.feed.FeedManager.update_feed")
def test_update_feed(mocked_update_feed, graphql_request):
    uuid = fake.uuid4()
    response = graphql_request(
        graphql_request_data={
            "query": update_feed,
            "variables": {"uuid": uuid},
        }
    )
    assert response["data"]["updateFeed"]["success"]
    assert mocked_update_feed.called_once_with(uuid)


@pytest.mark.django_db
@mock.patch("feeds.models.feed.FeedManager.delete_feed")
def test_delete_feed(mocked_delete_feed, graphql_request, user):
    uuid = fake.uuid4()
    response = graphql_request(
        graphql_request_data={
            "query": delete_feed,
            "user": user,
            "variables": {"uuid": uuid},
        }
    )
    assert response["data"]["deleteFeed"]["success"]
    assert "errors" not in response
    assert mocked_delete_feed.called_once_with(user, uuid)


@pytest.mark.django_db
@mock.patch("django.core.cache.cache.get")
def test_feed_update_state(mocked_cache, graphql_request, user):
    uuid = fake.uuid4()
    graphql_request(
        graphql_request_data={
            "query": feed_update_state,
            "user": user,
            "variables": {"uuid": uuid},
        }
    )
    uuid_hex = uuid.replace("-", "")
    key = f"{uuid_hex}_update_state_{user.id}"
    assert mocked_cache.called_with(key)


@pytest.mark.django_db
@mock.patch("feeds.models.following_feed.FollowingFeedManager.follow")
def test_follow_feed(mocked_follow_feed, graphql_request, user, feed):
    response = graphql_request(
        graphql_request_data={
            "query": follow_feed,
            "user": user,
            "variables": {"uuid": str(feed.uuid)},
        }
    )
    assert response["data"]["followFeed"]["success"]
    assert "errors" not in response
    assert mocked_follow_feed.called_once_with(user, feed.uuid)


@pytest.mark.django_db
@mock.patch("feeds.models.following_feed.FollowingFeedManager.unfollow")
def test_unfollow_feed(mocked_unfollow_feed, graphql_request, user, feed):
    graphql_request(
        graphql_request_data={
            "query": unfollow_feed,
            "user": user,
            "variables": {"uuid": str(feed.uuid)},
        }
    )
    assert mocked_unfollow_feed.called_once_with(user, feed.uuid)


@pytest.mark.django_db
@mock.patch("feeds.models.feed_item.FeedItem.mark_as_read")
def test_read_feed(mocked_read_item, graphql_request, user, feed_item):
    graphql_request(
        graphql_request_data={
            "query": read_item,
            "user": user,
            "variables": {"uuid": str(feed_item.uuid)},
        }
    )
    assert mocked_read_item.called_once_with(feed_item, user)


@pytest.mark.django_db
@mock.patch("feeds.models.feed_item.FeedItem.mark_as_unread")
def test_read_feed(mocked_unread_item, graphql_request, user, feed_item):
    graphql_request(
        graphql_request_data={
            "query": unread_item,
            "user": user,
            "variables": {"uuid": str(feed_item.uuid)},
        }
    )
    assert mocked_unread_item.called_once_with(feed_item, user)


@pytest.mark.django_db
def test_feed_query(graphql_request, feed_factory, user):
    for _ in range(10):
        feed_factory.create(
            url=fake.url(), user=user, is_active=True, last_updated=timezone.now()
        )
    response = graphql_request(
        graphql_request_data={
            "query": feed_query,
            "user": user,
            "variables": {"orderBy": "-lastUpdated"},
        }
    )
    assert len(response["data"]["feeds"]["edges"]) == 10
    first_result = response["data"]["feeds"]["edges"][0]["node"]["lastUpdated"]
    second_result = response["data"]["feeds"]["edges"][1]["node"]["lastUpdated"]

    assert first_result > second_result


@pytest.mark.django_db
def test_feed_item_query(graphql_request, feed_item_factory, user, feed):
    for _ in range(10):
        feed_item_factory.create(guid=fake.text(max_nb_chars=32), feed=feed)
    response = graphql_request(
        graphql_request_data={
            "query": feed_item_query,
            "user": user,
            "variables": {"orderBy": "-lastUpdated"},
        }
    )
    assert len(response["data"]["feedItems"]["edges"]) == 10

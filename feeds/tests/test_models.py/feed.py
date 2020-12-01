from unittest import mock

import pytest
from faker import Faker
from feeds.exceptions import FeedAlreadyRegistered, NoSuchFeedExist
from feeds.models import Feed

fake = Faker()


class FeedManagerTestCase:
    @staticmethod
    @pytest.mark.django_db
    @mock.patch("feeds.tasks.feed_updater")
    def test_register(mocked_feed_updater, user):
        url = fake.url()
        Feed.objects.create(url=url, user=user)
        assert mocked_feed_updater.not_called()

        with pytest.raises(FeedAlreadyRegistered):
            Feed.objects.register(url=url, user=user)
        assert mocked_feed_updater.not_called()

    @staticmethod
    @pytest.mark.django_db
    @mock.patch("feeds.tasks.feed_updater")
    def test_update(mocked_feed_updater):
        with pytest.raises(NoSuchFeedExist):
            uuid = fake.uuid4()
            Feed.objects.update_feed(uuid=uuid)
        assert mocked_feed_updater.not_called()

import pytest
from faker import Faker
from feeds.exceptions import FollowingFeedExist, NoSuchFeedExist, NotFollowingFeed
from feeds.models import FollowingFeed

fake = Faker()


@pytest.mark.django_db
def test_follow(feed, user):
    following_feed = FollowingFeed.objects.follow(user=user, feed_uuid=feed.uuid)
    assert following_feed.feed_id == feed.id

    with pytest.raises(FollowingFeedExist):
        FollowingFeed.objects.follow(user=user, feed_uuid=feed.uuid)

    with pytest.raises(NoSuchFeedExist):
        fake_uuid = fake.uuid4()
        FollowingFeed.objects.follow(user=user, feed_uuid=fake_uuid)

    assert FollowingFeed.objects.count() == 1

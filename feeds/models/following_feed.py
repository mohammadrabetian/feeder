from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feeds.models.feed import Feed

from ..exceptions import FollowingFeedExist, NoSuchFeedExist, NotFollowingFeed

User = get_user_model()


class FollowingFeedManager(models.Manager):
    def follow(self, user: User, feed_uuid: UUID):
        if self.filter(user=user, feed__uuid=feed_uuid).exists():
            raise FollowingFeedExist(_(f"You are already following this feed"))
        try:
            feed = Feed.objects.get(uuid=feed_uuid)
            return self.create(user=user, feed=feed)
        except Feed.DoesNotExist:
            raise NoSuchFeedExist(_(f"There is no feed with {feed_uuid} id!"))

    def unfollow(self, user: User, feed_uuid: UUID):
        if not self.filter(user=user, feed__uuid=feed_uuid).exists():
            raise NotFollowingFeed(
                _(f"You are not following the feed with {feed_uuid} id!")
            )
        self.get(user=user, feed__uuid=feed_uuid).delete()


class FollowingFeed(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="following_feeds"
    )
    feed = models.ForeignKey(
        "feeds.Feed", on_delete=models.CASCADE, related_name="followers"
    )
    objects = FollowingFeedManager()

    class Meta:
        app_label = "feeds"
        constraints = [
            models.UniqueConstraint(fields=["user", "feed"], name="follow_feed_once")
        ]

    def __str__(self) -> str:
        return f"{self.user.username} following {self.feed.uuid}"

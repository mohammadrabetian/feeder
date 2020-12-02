from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models


class ReadItem(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    user = models.ForeignKey(
        get_user_model(), related_name="read_items", on_delete=models.CASCADE
    )
    feed_item = models.ForeignKey(
        "feeds.FeedItem", related_name="reads", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "feeds"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "feed_item"], name="unique_read_item_per_user"
            )
        ]

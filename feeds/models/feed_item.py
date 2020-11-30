from typing import Union
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from feedparser import FeedParserDict
from feeds.helpers import convert_time
from feeds.models import Feed


class FeedItemManager(models.Manager):
    def update_or_create_entry(
        self, entry: FeedParserDict, feed: Feed
    ) -> Union[int, "FeedItem"]:
        kwargs = dict()
        kwargs["title"] = entry.get("title")
        kwargs["content"] = (
            entry.get("description")
            or entry.get("content", [{"value": ""}])[0]["value"]
        )
        kwargs["comments_url"] = entry.get("comments")
        kwargs["date_modified"] = convert_time(
            entry.get("updated_parsed") or entry.get("published_parsed", timezone.now())
        )

        if self.filter(feed=feed, guid=entry.guid).exists():
            return self.filter(feed=feed, guid=entry.guid).update(**kwargs)

        kwargs["feed"] = feed
        kwargs["url"] = entry.get("link")
        kwargs["guid"] = entry.guid
        return self.create(**kwargs)


class FeedItem(models.Model):
    """A feed contains a collection of items. This model stores them."""

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    feed = models.ForeignKey(
        "feeds.Feed", related_name="items", on_delete=models.CASCADE
    )
    title = models.CharField(_("Title"), max_length=255, db_index=True)
    url = models.URLField(_("Url"), max_length=1000)
    guid = models.CharField(_("Guid"), max_length=32, db_index=True)
    content = models.TextField(_("Content"))
    comments_url = models.URLField(_("Comments URL"), blank=True, null=True)

    date_modified = models.DateTimeField(
        _("Date modified"), null=True, blank=True, db_index=True
    )
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    # used to check an item as read/unread
    read = models.BooleanField(default=False)
    objects = FeedItemManager()

    class Meta:
        app_label = "feeds"
        verbose_name = _("Feed Item")
        verbose_name_plural = _("Feed Items")
        ordering = ("-created_at", "-date_modified")
        constraints = [
            models.UniqueConstraint(
                fields=["feed", "guid"], name="unique_guid_per_feed"
            )
        ]

    def __str__(self) -> str:
        return f"{self.title} [{self.feed.title}]"

    def mark_as_read(self) -> None:
        if not self.read:
            self.read = True
            self.save(update_fields=["read"])

    def mark_as_unread(self) -> None:
        if self.read:
            self.read = False
            self.save(update_fields=["read"])

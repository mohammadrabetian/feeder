import textwrap
from uuid import UUID, uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..exceptions import FeedAlreadyRegistered, NoSuchFeedExist
from ..helpers import validate_url
from ..tasks import feed_updater

User = get_user_model()


class FeedManager(models.Manager):
    def register(self, url: str, user: User):
        if self.filter(url=url, user=user).exists():
            raise FeedAlreadyRegistered(_(f"{url} is already registered"))
        url = validate_url(url)
        feed = self.create(url=url, user=user)
        feed_updater.apply_async(kwargs={"feed_id": feed.id})
        return feed

    def update_feed(self, uuid: UUID):
        try:
            feed = self.get(uuid=uuid)
            feed_updater.apply_async(kwargs={"feed_id": feed.id})
        except self.model.DoesNotExist:
            raise NoSuchFeedExist(_(f"There is no feed with {uuid} id"))

    def delete_feed(self, uuid: UUID, user: User):
        try:
            feed = self.get(uuid=uuid, user=user)
            feed.delete()
        except self.model.DoesNotExist:
            raise NoSuchFeedExist(_(f"There is no feed with {uuid} id"))


class Feed(models.Model):
    """All of these fields are from Feedparser's Feed object"""

    # used for api calls
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="feeds"
    )
    url = models.URLField(_("Url"))
    title = models.CharField(
        _("Title"), max_length=255, db_index=True, blank=True, null=True
    )
    subtitle = models.TextField(_("Subtitle"), blank=True, null=True)
    rights = models.CharField(_("Rights"), max_length=255, blank=True, null=True)
    info = models.CharField(_("Infos"), max_length=255, blank=True, null=True)
    language = models.CharField(_("Language"), max_length=50, blank=True, null=True)
    guid = models.CharField(
        _("Global Unique Identifier"),
        max_length=32,
        blank=True,
        null=True,
        db_index=True,
    )
    icon_url = models.URLField(_("Icon URL"), blank=True, null=True)
    image_url = models.URLField(_("Image URL"), blank=True, null=True)
    last_modified = models.DateTimeField(
        _("Last modified"), null=True, blank=True, db_index=True
    )
    # datetime when the feed was updated by last time
    last_updated = models.DateTimeField(_("Last updated"), null=True, blank=True)
    # used to define valid rss feeds
    is_active = models.BooleanField(default=False)

    objects = FeedManager()

    class Meta:
        app_label = "feeds"
        verbose_name = _("Feed")
        verbose_name_plural = _("Feeds")
        constraints = [
            models.UniqueConstraint(fields=["url", "user"], name="unique_feed_per_user")
        ]

    def __str__(self) -> str:
        return str(self.uuid)

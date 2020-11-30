import logging
from hashlib import md5

from celery import Task, shared_task
from celery.result import AsyncResult
from django.apps import apps
from django.core.cache import cache
from django.utils import timezone

from .helpers import convert_time, request_feed

logger = logging.getLogger(__name__)


class BaseTask(Task):
    """Celery base task class to handle logics needed on each state.
    Methods in this class will update the state of updating a feed in
    cache. It is meant to be a simple way to inform client on feed update
    states.

    Args:
        Task on_success: Will update cache with <<SUCCESS>> value.
        Task on_failure: Will update cache with <<FAILURE-REASON>> value.
        Task on_retry: Will update cache with <<RETRYING-REASON>> value.
    """

    def on_success(self, retval, task_id, args, kwargs) -> None:
        feed_model = apps.get_model("feeds", "Feed")
        logger.info("success on %s, writing state to cache", task_id)
        feed = feed_model.objects.get(id=kwargs.get("feed_id"))
        key = f"{feed.uuid}_update_state_{feed.user_id}"
        value = "SUCCESS"
        cache.set(key=key, value=value, timeout=30)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        feed_model = apps.get_model("feeds", "Feed")
        logger.info("failure on %s, writing state to cache", task_id)
        feed = feed_model.objects.get(id=kwargs.get("feed_id"))
        key = f"{feed.uuid}_update_state_{feed.user_id}"
        value = f"FAILURE-{exc}"
        cache.set(key=key, value=value, timeout=30)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        feed_model = apps.get_model("feeds", "Feed")
        logger.info("retrying on %s, writing state to cache", task_id)
        feed = feed_model.objects.get(id=kwargs.get("feed_id"))
        key = f"{feed.uuid}_update_state_{feed.user_id}"
        value = f"RETRYING-{exc}"
        cache.set(key=key, value=value, timeout=30)


@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 4, "countdown": 10},
    base=BaseTask,
)
def feed_updater(feed_id: int) -> AsyncResult:
    """Update feed with each item in the feed.

    Args:
        feed_id (int): Registered feed id.

    Returns:
        AsyncResult
    """
    feed_model = apps.get_model("feeds", "Feed")
    feed_item_model = apps.get_model("feeds", "FeedItem")

    feed = feed_model.objects.get(id=feed_id)

    document = request_feed(feed.url)
    guid = md5(document.feed.get("link").encode("utf-8")).hexdigest()

    feed.subtitle = document.feed.get("subtitle")
    feed.rights = document.feed.get("rights") or document.feed.get("license")
    feed.info = document.feed.get("info")
    feed.guid = guid
    feed.image_url = document.feed.get("image", {}).get("href")
    feed.icon_url = document.feed.get("icon")
    feed.language = document.feed.get("language")

    last_modified = convert_time(document.get("updated_parsed", timezone.now()))
    feed.last_modified = last_modified

    feed.last_updated = timezone.now()
    feed.is_active = True
    feed.save()

    for entry in document.entries:
        entry.guid = md5(entry.get("link").encode("utf-8")).hexdigest()
        feed_item_model.objects.update_or_create_entry(entry=entry, feed=feed)

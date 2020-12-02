from hashlib import md5

import pytest
from feedparser import FeedParserDict
from feeds.models import FeedItem


class FeedItemManagerTestCase:
    entry = FeedParserDict()
    entry["title"] = "Just in Case"
    entry["description"] = "Some cool content"
    entry["link"] = "http://cool.com"

    @pytest.mark.django_db
    def test_update_or_create_entry(self, feed):
        self.entry.guid = md5(self.entry.get("link").encode("utf-8")).hexdigest()
        feed_item = FeedItem.objects.update_or_create_entry(entry=self.entry, feed=feed)
        assert feed_item.feed_id == feed.id
        result = FeedItem.objects.update_or_create_entry(entry=self.entry, feed=feed)
        assert result == 1


class FeedItemModelTestCase:
    @staticmethod
    @pytest.mark.django_db
    def test_mark_as_read(feed_item):
        assert not feed_item.read
        feed_item.mark_as_read()
        feed_item.refresh_from_db()
        assert feed_item.read

    @staticmethod
    @pytest.mark.django_db
    def test_mark_as_unread(feed_item):
        feed_item.mark_as_read()
        feed_item.refresh_from_db()
        assert feed_item.read
        feed_item.mark_as_unread()
        feed_item.refresh_from_db()
        assert not feed_item.read

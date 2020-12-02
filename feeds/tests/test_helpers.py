import pytest
from django.core.exceptions import ValidationError
from faker import Faker
from feedparser import FeedParserDict
from feeds.exceptions import NotValidFeedUrl
from feeds.helpers import request_feed, validate_url
from requests.exceptions import ConnectionError, ReadTimeout

fake = Faker()


def test_request_feed_exceptions():
    fake_url = fake.url()
    with pytest.raises((ConnectionError, ReadTimeout, NotValidFeedUrl)):
        request_feed(feed_url=fake_url)


def test_request_feed_return_value():
    feed_url = "http://joeroganexp.joerogan.libsynpro.com/rss"
    response = request_feed(feed_url=feed_url)
    assert isinstance(response, FeedParserDict)
    assert not response.bozo


def test_validate_url():
    invalid_url = "ObviouslyFake"
    with pytest.raises(ValidationError):
        validate_url(invalid_url)

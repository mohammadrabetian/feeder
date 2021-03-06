import logging
from datetime import datetime
from io import BytesIO
from time import mktime, struct_time
from typing import Union
from uuid import UUID

import feedparser
import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _
from feedparser import FeedParserDict

from .exceptions import NotValidFeedUrl

logger = logging.getLogger(__name__)


def request_feed(feed_url: str) -> FeedParserDict:
    """Using this function for sepration of concerns between application
    logic and dependencies.
    Using only feedparser as http request can cause problems.

    Args:
        feed_url (str)

    Raises:
        NotValidFeedUrl
        ReadTimeout
        ConnectionError

    Returns:
        FeedParserDict: A feedparser dict containing feed and feed items.
    """
    try:
        resp = requests.get(feed_url, timeout=5)
    except requests.ReadTimeout:
        logger.warning("Timeout when reading RSS %s", feed_url)
        raise requests.ReadTimeout(f"Read Timeout error for {feed_url}")
    except requests.ConnectionError:
        logger.warning("Not known service %s", feed_url)
        raise requests.ConnectionError(f"{feed_url} is not known")

    content = BytesIO(resp.content)
    document = feedparser.parse(content)

    # given url is not a valid rss feed
    if document.bozo:
        raise NotValidFeedUrl(_(f"{feed_url} is not a valid rss feed"))

    return document


def convert_time(time: Union[struct_time, datetime]) -> datetime:
    """FeedParserDict items contain struct_time.
    This function will convert them to standard datetime format.

    Args:
        time (Union[struct_time, datetime])

    Returns:
        datetime
    """
    if isinstance(time, struct_time):
        time = datetime.fromtimestamp(mktime(time))
    return time


def validate_url(url: str) -> str:
    """Default validations do not work on models if we use
    custom manager methods.
    There are few other ways to do this, but this seems the
    simplest to implement.

    Args:
        url (str)

    Raises:
        ValidationError

    Returns:
        str: valid url.
    """
    validate = URLValidator()
    try:
        validate(url)
        return url
    except ValidationError:
        raise ValidationError(_("Please enter a valid url"))


def validate_uuid4(uuid_string: str) -> bool:
    """A simple helper to check uuid validation in
    custom filters through apis.

    Args:
        uuid_string ([str])

    Returns:
        [bool]
    """
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return True

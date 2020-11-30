class FeedException(Exception):
    """Exception class related to Feeds"""


class NotValidFeedUrl(FeedException):
    """Raised when url is not a valid rss feed"""


class FollowingFeedExist(FeedException):
    """Raised when user is already following feed upon request"""


class NoSuchFeedExist(FeedException):
    """Raise when requesting a feed which does not exist"""


class NoSuchFeedItemExist(FeedException):
    """Raise when requesting a feed item which does not exist"""


class NotFollowingFeed(FeedException):
    """Raised upon unfollow request while not actually following"""


class FeedAlreadyRegistered(FeedException):
    """Raised upon register request for duplicate url"""

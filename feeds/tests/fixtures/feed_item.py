import factory
from feeds.models import FeedItem

from .feed import FeedFactory


class FeedItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeedItem

    feed = factory.SubFactory(FeedFactory)
    url = factory.Faker("url")

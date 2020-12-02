import factory
from accounts.tests.fixtures import UserFactory
from feeds.models import Feed


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feed

    user = factory.SubFactory(UserFactory)
    url = factory.Faker(
        "random_element",
        elements=[
            "http://www.nu.nl/rss/Algemeen",
            "http://joeroganexp.joerogan.libsynpro.com/rss",
        ],
    )

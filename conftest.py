from pytest_factoryboy import register

from accounts.tests.fixtures import UserFactory
from feeder.tests import graphql_request, set_celery_eager_false
from feeds.tests.fixtures import FeedFactory

register(UserFactory)
register(FeedFactory)

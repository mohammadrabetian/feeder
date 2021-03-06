import logging

import django_filters
import graphene
from accounts.schema import UserType
from django.core.cache import cache
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .exceptions import NoSuchFeedItemExist
from .helpers import validate_uuid4
from .models import Feed, FeedItem, FollowingFeed, ReadItem

logger = logging.getLogger(__name__)


class FeedType(DjangoObjectType):
    uuid = graphene.UUID()
    user = graphene.Field(UserType)
    url = graphene.String()
    title = graphene.String()
    subtitle = graphene.String()
    rights = graphene.String()
    info = graphene.String()
    language = graphene.String()
    guid = graphene.String()
    icon_url = graphene.String()
    image_url = graphene.String()
    last_modified = graphene.DateTime()
    last_updated = graphene.DateTime()

    class Meta:
        model = Feed
        filter_fields = []
        interfaces = (relay.Node,)


class FeedItemType(DjangoObjectType):
    feed = graphene.Field(FeedType)
    title = graphene.String()
    url = graphene.String()
    guid = graphene.String()
    content = graphene.String()
    comments_url = graphene.String()
    date_modified = graphene.DateTime()

    class Meta:
        model = FeedItem
        filter_fields = []
        interfaces = (relay.Node,)


class FeedItemFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("request").user
        super().__init__(*args, **kwargs)

    feed = django_filters.CharFilter(method="feed_filter")
    read = django_filters.BooleanFilter(method="read_filter")
    order_by = django_filters.OrderingFilter(
        fields=(("feed__last_updated", "lastUpdated"),)
    )

    def read_filter(self, queryset, value, *args, **kwargs):
        if value and True in args:
            return queryset.filter(reads__user=self.user)
        return queryset

    def feed_filter(self, queryset, value, *args, **kwargs):
        if value and validate_uuid4(args[0]):
            return queryset.filter(feed__uuid=args[0])
        return queryset

    class Meta:
        model = FeedItem
        fields = ["feed"]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(
            Q(feed__user=self.request.user)
            | Q(feed__followers__user=self.request.user),
        ).select_related("feed")


class FeedFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(fields=(("last_updated", "lastUpdated"),))

    class Meta:
        model = Feed
        fields = ["title"]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(
            Q(user=self.request.user) | Q(followers__user=self.request.user),
            is_active=True,
        ).select_related("user")


class FeedQuery:
    feeds = DjangoFilterConnectionField(FeedType, filterset_class=FeedFilter)
    feed_items = DjangoFilterConnectionField(
        FeedItemType, filterset_class=FeedItemFilter
    )


class FeedUpdateStateQuery:
    """Used as polling to define feed update state.
    Uses cache on each polling for better performance and space
    allocation.

    Returns:
        [str]: A string for representing feed update status.
    """

    update_state = graphene.String(uuid=graphene.UUID(required=True))

    def resolve_update_state(self, info, uuid):
        key = f"{uuid.hex}_update_state_{info.context.user.id}"
        result = cache.get(key)
        if result:
            return result
        return f"No update state for {uuid}"


class RegisterFeed(graphene.Mutation):
    class Arguments:
        url = graphene.String(required=True)

    feed = graphene.Field(FeedType)

    def mutate(self, info, url):
        feed = Feed.objects.register(url=url, user=info.context.user)
        return RegisterFeed(feed=feed)


class UpdateFeed(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        Feed.objects.update_feed(uuid)
        return UpdateFeed(success=True)


class DeleteFeed(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        Feed.objects.delete_feed(uuid=uuid, user=info.context.user)
        return DeleteFeed(success=True)


class FollowFeed(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        FollowingFeed.objects.follow(user=info.context.user, feed_uuid=uuid)
        return FollowFeed(success=True)


class UnFollowFeed(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        FollowingFeed.objects.unfollow(user=info.context.user, feed_uuid=uuid)
        return UnFollowFeed(success=True)


class ReadFeedItem(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        try:
            feed_item = FeedItem.objects.get(uuid=uuid)
            feed_item.mark_as_read(user=info.context.user)
            return ReadFeedItem(success=True)
        except FeedItem.DoesNotExist:
            raise NoSuchFeedItemExist(_(f"There is no feed item with {uuid} id!"))


class UnReadFeedItem(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, uuid):
        try:
            feed_item = FeedItem.objects.get(uuid=uuid)
            feed_item.mark_as_unread(user=info.context.user)
            return ReadFeedItem(success=True)
        except FeedItem.DoesNotExist:
            raise NoSuchFeedItemExist(_(f"There is no feed item with {uuid} id!"))


class FeedsMutations(object):
    register_feed = RegisterFeed.Field()
    follow_feed = FollowFeed.Field()
    unfollow_feed = UnFollowFeed.Field()
    read_feed_item = ReadFeedItem.Field()
    unread_feed_item = UnReadFeedItem.Field()
    update_feed = UpdateFeed.Field()
    delete_feed = DeleteFeed.Field()

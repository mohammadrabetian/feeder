import graphene
from accounts.schema import AccountsMutations
from feeds.schema import FeedQuery, FeedsMutations, FeedUpdateStateQuery


class Query(graphene.ObjectType, FeedQuery, FeedUpdateStateQuery):
    node = graphene.relay.Node.Field()


class Mutations(graphene.ObjectType, FeedsMutations, AccountsMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)

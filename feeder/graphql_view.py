from django.conf import settings
from graphene_django.views import GraphQLView

from accounts.graphql_middleware import FeederAuthMiddleWare
from .schema import schema

class FeederGraphQLView(GraphQLView):
    """Custom GraphQL view to inject custom middlewares.

    Args:
        GraphQLView ([type])
    """

    def __init__(self, *args, **kwargs):
        middleware = kwargs.get("middleware", [])
        middleware.append(FeederAuthMiddleWare)
        kwargs["middleware"] = middleware
        kwargs["graphiql"] = settings.DEBUG
        kwargs["schema"] = schema
        super().__init__(*args, **kwargs)

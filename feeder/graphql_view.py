from django.conf import settings
from graphene_django.views import GraphQLView


class FeederGraphQLView(GraphQLView):
    """Custom GraphQL view to inject custom middlewares.

    Args:
        GraphQLView ([type])
    """

    def __init__(self, *args, **kwargs):
        middleware = kwargs.get("middleware", [])

        kwargs["middleware"] = middleware
        kwargs["graphiql"] = settings.DEBUG
        super().__init__(*args, **kwargs)

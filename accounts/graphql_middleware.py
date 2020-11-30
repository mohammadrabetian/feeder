from django.utils.translation import ugettext_lazy as _

from .exceptions import NotLoggedIn


class FeederAuthMiddleWare:
    """AuthMiddleware for GraphQL to check user
    authentication upon requests.
    This app has functionalities that needs for a user
    to be authenticated.

    Raises:
        NotLoggedIn

    """

    # Paths user can access without authentication
    not_required_login_paths = [
        "login",
        "logout",
        "register",
    ]

    def resolve(self, next, root, info, **args):
        if info.path[0] in self.not_required_login_paths:
            return next(root, info, **args)
        elif info.context.user.is_authenticated:
            return next(root, info, **args)
        else:
            raise NotLoggedIn(_("You should be logged in!"))

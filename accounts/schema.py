import graphene
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.utils.translation import gettext_lazy as _
from graphene import relay
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError


class UserType(DjangoObjectType):
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    full_name = graphene.String(source="get_full_name")
    email = graphene.String()

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
            "id",
        ]
        interfaces = (relay.Node,)


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    username = graphene.String()

    def mutate(self, info, username, password):
        if not info.context.user.is_authenticated:
            user = authenticate(
                info.context,
                username=username,
                password=password,
            )
            if user is None:
                raise GraphQLError(_("Credentials are incorrect"))

            login(info.context, user)
            return Login(success=True, username=user.username)
        raise GraphQLError(_("You are already logged in"))


class Logout(graphene.Mutation):

    success = graphene.Boolean()

    def mutate(self, info):
        if info.context.user.is_authenticated:
            logout(info.context)
            return Logout(success=True)
        raise GraphQLError(_("You are not logged in"))


class RegisterInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    name = graphene.String(required=False)
    email = graphene.String(required=False)
    password = graphene.String(required=True)


class Register(graphene.Mutation):
    class Arguments:
        register_info = RegisterInput(required=True)

    success = graphene.Boolean()
    username = graphene.String()

    def mutate(self, info, register_info):
        user_model = get_user_model()
        if user_model.objects.filter(
            username__iexact=register_info.get("username")
        ).exists():
            raise GraphQLError(
                _(f"User with username {register_info.get('username')} exists")
            )
        user = user_model(**register_info)
        user.set_password(register_info.get("password"))
        user.save()
        login(info.context, user)
        return Register(success=True, username=user.username)


class AccountsMutations(object):
    register = Register.Field()
    login = Login.Field()
    logout = Logout.Field()

import pytest
from celery import current_app
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from graphene.test import Client

from ..schema import schema


@pytest.fixture
def graphql_request():
    return get_graphql_response


def get_graphql_response(graphql_request_data):
    # creating the Client
    client = Client(schema)
    # creating the Context
    context = generate_context(
        user=graphql_request_data.get("user", None),
    )
    variables = graphql_request_data.get("variables", None)
    graphql_response = client.execute(
        graphql_request_data["query"],
        variable_values=variables,
        context_value=context,
    )
    return graphql_response


def generate_context(user):
    context = generate_request(url="/graphql/", user=user)
    return context


def generate_request(url, user=None):
    request = RequestFactory().post(url)
    set_request_session(request)
    set_request_user(request, user)
    return request


def set_request_session(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()


def set_request_user(request, user):
    if user:
        setattr(request, "user", user)


@pytest.fixture
def set_celery_eager_false():
    current_app.conf.task_always_eager = True

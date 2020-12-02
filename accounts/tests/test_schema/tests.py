import pytest
from faker import Faker

from .queries import logout_user, register_user

fake = Faker()


@pytest.mark.django_db
def test_register(graphql_request):
    response = graphql_request(
        graphql_request_data={
            "query": register_user,
            "variables": {
                "registerInfo": {"username": fake.name(), "password": fake.password()}
            },
        }
    )
    assert response["data"]["register"]["success"]


@pytest.mark.django_db
def test_logout(graphql_request, user):
    response = graphql_request(
        graphql_request_data={
            "query": logout_user,
            "user": user,
        }
    )
    assert response["data"]["logout"]["success"]

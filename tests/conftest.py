import pytest
from helpers.api_client import *
from helpers.helpers import generate_random_register_data_for_user


@pytest.fixture()
def create_and_delete_user():
    create_payload = generate_random_register_data_for_user()[0]

    response = ApiClientMethods.create_user(create_payload)
    auth_token = ApiClientMethods.get_auth_token(response)

    yield create_payload, auth_token

    ApiClientMethods.delete_user(auth_token)

@pytest.fixture()
def create_user_only():
    create_payload, login_payload = generate_random_register_data_for_user()

    response = ApiClientMethods.create_user(create_payload)
    auth_token = ApiClientMethods.get_auth_token(response)

    return login_payload, auth_token

@pytest.fixture()
def delete_user_only():
    auth_token = None

    def get_auth_token_for_delete(response):
        nonlocal auth_token
        auth_token = ApiClientMethods.get_auth_token(response)
        return auth_token

    yield get_auth_token_for_delete

    ApiClientMethods.delete_user(auth_token)

import allure
import pytest
from data.data import DataForTests
from helpers.api_client import ApiClientMethods
from helpers.helpers import generate_random_register_data_for_user


class TestApiCreateUser:
    @allure.title("Проверка успешного создания пользователя с обязательными полями")
    def test_create_user_with_valid_data_return_200(self, delete_user_only):
        create_payload = generate_random_register_data_for_user()[0]
        response = ApiClientMethods.create_user(create_payload)
        delete_user_only["auth_token"] = ApiClientMethods.get_auth_token(response)

        assert response.status_code == 200
        assert response.json()["success"] == True

    @allure.title("Проверка невозможности создания дубликата пользователя")
    def test_cannot_create_duplicate_user_returns_403(self, create_and_delete_user):
        create_payload = create_and_delete_user[0]
        expected_message = "User already exists"
        response = ApiClientMethods.create_user(create_payload)

        assert response.status_code == 403
        assert response.json()["success"] == False
        assert response.json()["message"] == expected_message

    @allure.title("Проверка невозможности создания пользователя с незаполненными обязательными полями")
    @pytest.mark.parametrize("payload", DataForTests.REGISTRATION_DATA_EMPTY_FIELDS, ids=["empty_email", "empty_password", "empty_name"])
    def test_cannot_create_user_with_empty_required_field_returns_403(self, payload):
        expected_message = "Email, password and name are required fields"
        response = ApiClientMethods.create_user(payload)

        assert response.status_code == 403
        assert response.json()["success"] == False
        assert response.json()["message"] == expected_message

class TestLoginUser:
    @allure.title("Проверка успешного логина под существующем пользователем")
    def test_user_can_login_with_valid_login_data_returns_200(self, create_user_only):
        login_payload = create_user_only[0]
        auth_token = create_user_only[1]
        response = ApiClientMethods.login_user(login_payload)

        assert response.status_code == 200
        assert response.json()["success"] == True

        ApiClientMethods.delete_user(auth_token)

    @allure.title("Проверка невозможности логина пользователя с неверным логином или паролем")
    def test_user_cannot_login_with_wrong_login_or_password_returns_401(self, create_and_delete_user):
        expected_message = "email or password are incorrect"
        correct_email = create_and_delete_user[0]["email"]
        correct_password = create_and_delete_user[0]["password"]

        wrong_payloads = ApiClientMethods.get_wrong_login_payloads(correct_email, correct_password)
        ApiClientMethods.assert_user_cannot_login_with_payloads(wrong_payloads, expected_message)

class TestCreateOrder:
    @allure.title("Проверка создания заказа авторизированным пользователем с ингредиентами, без ингредиентов и с несуществующим ингредиентом")
    @pytest.mark.parametrize("payload", DataForTests.CREATE_ORDER_WITH_VARIOUS_INGREDIENTS, ids=["with_ingredients", "empty_ingredients", "nonexistent_ingredients"])
    def test_create_order_with_auth_various_ingredients(self, create_and_delete_user, payload):
        auth_token = create_and_delete_user[1]
        response = ApiClientMethods.create_order(payload["ingredients"], auth_token)

        assert response.status_code == payload["expected_status_code"]
        if payload["expected_success"] is not None:
            assert response.json()["success"] == payload["expected_success"]

        if payload["expected_message"] is not None:
            assert response.json()["message"] == payload["expected_message"]

    @allure.title("Проверка создания заказа с неавторизированным пользователем с ингредиентами, без ингредиентов и с несуществующим ингредиентом")
    @pytest.mark.parametrize("payload",DataForTests.CREATE_ORDER_WITH_VARIOUS_INGREDIENTS, ids=["with_ingredients", "empty_ingredients", "nonexistent_ingredients"])
    def test_create_order_without_auth_various_ingredients(self, payload):
        response = ApiClientMethods.create_order(payload["ingredients"])

        assert response.status_code == payload["expected_status_code"]
        if payload["expected_success"] is not None:
            assert response.json()["success"] == payload["expected_success"]

        if payload["expected_message"] is not None:
            assert response.json()["message"] == payload["expected_message"]

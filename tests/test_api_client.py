import allure
import pytest
from data.data import DataForTests
from helpers.api_client import ApiClientMethods
from helpers.helpers import generate_random_register_data_for_user, generate_random_ingredient_hash


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
    @allure.title("Проверка создания заказа авторизированным пользователем и с ингредиентами")
    def test_create_order_with_auth_and_with_ingredients_returns_200(self, create_and_delete_user):
        auth_token = create_and_delete_user[1]
        ingredient = ApiClientMethods.get_random_ingredients()
        response = ApiClientMethods.create_order(ingredient, auth_token)

        assert response.status_code == 200
        assert response.json()["success"] == True

    @allure.title("Проверка создания заказа авторизированным пользователем и без ингредиентов")
    def test_create_order_with_auth_and_without_ingredients_returns_400(self, create_and_delete_user):
        auth_token = create_and_delete_user[1]
        expected_message = "Ingredient ids must be provided"
        ingredient = []
        response = ApiClientMethods.create_order(ingredient, auth_token)

        assert response.status_code == 400
        assert response.json()["success"] == False
        assert response.json()["message"] == expected_message

    @allure.title("Проверка создания заказа авторизированным пользователем и с несуществующим ингредиентом")
    def test_create_order_with_auth_and_with_nonexistent_ingredient_returns_500(self, create_and_delete_user):
        auth_token = create_and_delete_user[1]
        ingredient = generate_random_ingredient_hash()
        response = ApiClientMethods.create_order(ingredient, auth_token)

        assert response.status_code == 500

    @allure.title("Проверка создания заказа с неавторизированным пользователем и с ингредиентами")
    def test_create_order_without_auth_and_with_ingredients_returns_200(self):
        ingredient = ApiClientMethods.get_random_ingredients()
        response = ApiClientMethods.create_order(ingredient)

        assert response.status_code == 200
        assert response.json()["success"] == True

    @allure.title("Проверка создания заказа с неавторизированным пользователем и без ингредиентов")
    def test_create_order_without_auth_and_without_ingredients_returns_400(self):
        expected_message = "Ingredient ids must be provided"
        ingredient = []
        response = ApiClientMethods.create_order(ingredient)

        assert response.status_code == 400
        assert response.json()["success"] == False
        assert response.json()["message"] == expected_message

    @allure.title("Проверка создания заказа с неавторизированным пользователем и с несуществующим ингредиентом")
    def test_create_order_without_auth_and_with_nonexistent_ingredient_returns_500(self):
        ingredient = generate_random_ingredient_hash()
        response = ApiClientMethods.create_order(ingredient)

        assert response.status_code == 500

import random
import allure
import requests
from data.endpoints import Endpoints
from helpers.helpers import generate_random_number
from faker import Faker


class ApiClientMethods:
    @staticmethod
    @allure.step("Создаем пользователя")
    def create_user(payload):
        return requests.post(Endpoints.CREATE_USER, json=payload)

    @staticmethod
    @allure.step("Удаляем пользователя")
    def delete_user(auth_token=None):
        headers = {"Authorization": auth_token}
        return requests.delete(Endpoints.DELETE_USER, headers=headers)

    @staticmethod
    @allure.step("Логинимся в профиль пользователя")
    def login_user(payload):
        return requests.post(Endpoints.LOGIN_USER, json=payload)

    @staticmethod
    @allure.step("Создаем заказ")
    def create_order(payload, auth_token=None):
        headers = {}
        if auth_token:
            headers["Authorization"] = auth_token

        return requests.post(Endpoints.CREATE_ORDER, json=payload, headers=headers)

    @staticmethod
    @allure.step("Получаем данные для логина пользователя")
    def get_wrong_login_payloads(correct_email, correct_password):
        fake = Faker('ru_RU')
        return [
            {"email": correct_email, "password": fake.password(length=10)},
            {"email": fake.email(), "password": correct_password}
        ]

    @staticmethod
    @allure.step("Получаем список доступных ингредиентов")
    def get_ingredients_info():
        return requests.get(Endpoints.GET_INGREDIENTS_INFO)

    @staticmethod
    @allure.step("Выбираем случайные ингредиенты")
    def get_random_ingredients():
        ingredients_data = ApiClientMethods.get_ingredients_info().json()
        all_ingredients = ingredients_data.get("data", [])
        payload = {
            "ingredients": []
        }

        if all_ingredients:
            quantity = min(generate_random_number(10), len(all_ingredients))

            selected_ingredients = random.sample(all_ingredients, quantity)

            for ingredient in selected_ingredients:
                ingredient_id = ingredient.get("_id")
                if ingredient_id:
                    payload["ingredients"].append(ingredient_id)

        return payload

    @staticmethod
    @allure.step("Получаем токен авторизации")
    def get_auth_token(response):
        return response.json()["accessToken"]

from faker import Faker
from helpers.helpers import generate_random_register_data_for_user
from helpers.api_client import ApiClientMethods


class DataForTests:
    user_register_data = generate_random_register_data_for_user()[0]
    fake = Faker('ru_RU')

    REGISTRATION_DATA_EMPTY_FIELDS = [
        {
            "email": "",
            "password": user_register_data["password"],
            "name": user_register_data["name"]
        },
        {
            "email": user_register_data["email"],
            "password": "",
            "name": user_register_data["name"]
        },
        {
            "email": user_register_data["email"],
            "password": user_register_data["password"],
            "name": ""
        }
    ]

    CREATE_ORDER_WITH_VARIOUS_INGREDIENTS = [
        {
            "ingredients": {"ingredients": ApiClientMethods.get_random_ingredients()["ingredients"]},
            "expected_status_code": 200,
            "expected_success": True,
            "expected_message": None
        },
        {
            "ingredients": [],
            "expected_status_code": 400,
            "expected_success": False,
            "expected_message": "Ingredient ids must be provided"
        },
        {
            "ingredients": {"ingredients": fake.password(length=20)},
            "expected_status_code": 500,
            "expected_success": None,
            "expected_message": None
        }
    ]

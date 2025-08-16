from helpers.helpers import generate_random_register_data_for_user


class DataForTests:
    user_register_data = generate_random_register_data_for_user()[0]

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

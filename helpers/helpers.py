import random
from faker import Faker


def generate_random_register_data_for_user():
    fake = Faker('ru_RU')
    email = fake.email()
    password = fake.password(length=10)
    name = fake.name()

    create_payload = {
        "email": email,
        "password": password,
        "name": name
    }

    login_payload = {
        "email": email,
        "password": password
    }

    return create_payload, login_payload

def generate_random_number(number):
    return random.randint(1,number)

def generate_random_ingredient_hash():
    fake = Faker('ru_RU')
    ingredient = {"ingredients": fake.password(length=20)}
    return ingredient

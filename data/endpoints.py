BASE_URL = "https://stellarburgers.nomoreparties.site"

class Endpoints:
    CREATE_USER = f"{BASE_URL}/api/auth/register"
    LOGIN_USER = f"{BASE_URL}/api/auth/login"
    CREATE_ORDER = f"{BASE_URL}/api/orders"
    DELETE_USER = f"{BASE_URL}/api/auth/user"
    GET_INGREDIENTS_INFO = f"{BASE_URL}/api/ingredients"

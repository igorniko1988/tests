from faker import Faker

from framework.services.auth import AuthApi
from framework.transport.auth import BearerAuth
from framework.transport.client import ApiClient
from framework.user import LoggedInUser

fake = Faker()


def random_credentials() -> dict:
    """Случайные email и пароль для нового пользователя."""
    return {
        "email": f"{fake.user_name()}.{fake.random_int(100000, 999999)}@example.com",
        "password": fake.password(length=12),
    }


def create_user(base_url: str, timeout: float = 10) -> LoggedInUser:
    """Регистрирует нового пользователя и возвращает его с авторизованным клиентом."""
    credentials = random_credentials()

    # 1. Регистрация и логин — обычным клиентом без токена
    with ApiClient(base_url, timeout) as client:
        auth = AuthApi(client)
        auth.register(credentials).raise_for_status()
        token = auth.login(credentials).json()["access_token"]

    # 2. Личный клиент пользователя — с токеном внутри
    user_client = ApiClient(base_url, timeout, auth=BearerAuth(token))
    return LoggedInUser(credentials["email"], user_client)

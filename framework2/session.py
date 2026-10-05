from decimal import Decimal

from faker import Faker

from framework2.api.auth import AuthApi
from framework2.api.balances import BalancesApi
from framework2.api.orders import OrdersApi
from framework2.client import ApiClient
from framework2.config import Config
from framework2.models.balance import Balance

fake = Faker()


class UserSession:
    """Залогиненный пользователь: свой клиент с токеном и все API от его имени."""

    def __init__(self, email: str, password: str, client: ApiClient):
        self.email = email
        self.password = password
        self.client = client
        self.auth = AuthApi(client)
        self.balances = BalancesApi(client)
        self.orders = OrdersApi(client)

    def balance(self, asset: str) -> Balance:
        balances = [Balance.model_validate(b) for b in self.balances.get_all().json()]
        empty = Balance(asset=asset, available=Decimal(0), locked=Decimal(0))
        return next((b for b in balances if b.asset == asset), empty)

    def close(self) -> None:
        self.client.close()


def new_credentials() -> tuple[str, str]:
    email = f"{fake.user_name()}.{fake.random_int(100000, 999999)}@example.com"
    return email, fake.password(length=12)


def register_user(config: Config) -> UserSession:
    """Регистрирует нового пользователя, логинится и возвращает его сессию."""
    email, password = new_credentials()
    client = ApiClient(config.base_url, config.timeout)
    auth = AuthApi(client)

    auth.register(email, password).raise_for_status()
    login = auth.login(email, password)
    login.raise_for_status()

    client.set_token(login.json()["access_token"])
    return UserSession(email, password, client)

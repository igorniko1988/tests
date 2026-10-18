import pytest
from faker import Faker

faker = Faker()


@pytest.fixture
def credentials() -> dict[str, str]:
    return {"email": faker.unique.email(), "password": faker.password()}


@pytest.fixture(params=['USDT','BTC','ETH'])
def asset(request: pytest.FixtureRequest):
    return request.param
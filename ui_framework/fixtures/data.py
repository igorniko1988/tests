import pytest

from ui_framework.data.generators import credentials as generate_credentials


@pytest.fixture
def credentials() -> dict[str, str]:
    return generate_credentials()


@pytest.fixture(params=['USDT', 'BTC', 'ETH'])
def asset(request: pytest.FixtureRequest):
    return request.param

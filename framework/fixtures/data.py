import pytest
from faker import Faker

@pytest.fixture()
def credentials():
    faker = Faker()
    data = {
        'email': faker.email(),
        'password': faker.password(length=12)
    }
    return data
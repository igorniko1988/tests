import pytest
from dataclasses import dataclass

@dataclass()
class User:
    age: int
    name: str | None = None


@pytest.fixture
def user(request):
    age = request.param
    user = User(age=age)
    return user

@pytest.mark.parametrize('user', [1,2,3], indirect=True)
def test_user(user):
    print(user)


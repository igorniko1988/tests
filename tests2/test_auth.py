from framework2.models.error import ErrorResponse
from framework2.models.user import Token, User
from framework2.session import new_credentials


def test_register_returns_user(auth_api):
    email, password = new_credentials()

    response = auth_api.register(email, password)

    assert response.status_code == 201
    assert User.model_validate(response.json()).email == email


def test_login_returns_token(auth_api):
    email, password = new_credentials()
    auth_api.register(email, password)

    response = auth_api.login(email, password)

    assert response.status_code == 200
    Token.model_validate(response.json())


def test_me_returns_own_profile(user):
    response = user.auth.me()

    assert response.status_code == 200
    assert User.model_validate(response.json()).email == user.email


def test_me_without_token_is_401(auth_api):
    response = auth_api.me()

    assert response.status_code == 401
    assert ErrorResponse.model_validate(response.json()).error.code == "unauthorized"


def test_register_same_email_twice_is_409(auth_api):
    email, password = new_credentials()
    auth_api.register(email, password)

    response = auth_api.register(email, password)

    assert response.status_code == 409
    assert ErrorResponse.model_validate(response.json()).error.code == "email_taken"

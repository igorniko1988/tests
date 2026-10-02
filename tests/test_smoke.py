from decimal import Decimal

import pytest


@pytest.mark.smoke
def test_health(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_registration(auth_api, user_credential):
    response = auth_api.register(user_credential)

    assert response.status_code == 201
    assert response.json()["email"] == user_credential["email"]
    assert "id" in response.json()


def test_register_with_the_same_creds(auth_api, user_credential):
    response = auth_api.register(user_credential)
    assert response.status_code == 201

    response = auth_api.register(user_credential)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "email_taken"


def test_login_auth(auth_api, user_credential):
    response = auth_api.register(user_credential)
    assert response.status_code == 201

    authorised_user = auth_api.login(user_credential)

    assert authorised_user.status_code == 200
    assert "access_token" in authorised_user.json()


def test_me_without_token(auth_api):
    me = auth_api.me()
    assert me.status_code == 401


def test_me(auth_api, user_credential, bearer_token):
    me = auth_api.me(auth=bearer_token)
    assert me.status_code == 200
    assert me.json()["email"] == user_credential["email"]


def test_login_with_incorrect_email(auth_api, user_credential):
    response = auth_api.register(user_credential)

    assert response.status_code == 201

    user_with_incorrect_email = {
        "email": "sadkasjdio@gmail.com",
        "password": user_credential["password"],
    }

    non_authorized_user = auth_api.login(user_with_incorrect_email)

    assert non_authorized_user.status_code == 401
    assert non_authorized_user.json()["error"]["message"] == "Invalid email or password"


def test_user_with_wrong_password(auth_api, user_credential):
    response = auth_api.register(user_credential)

    assert response.status_code == 201

    user_with_incorrect_password = {
        "email": user_credential["email"],
        "password": "WrongPassword1!",
    }

    non_authorized_user = auth_api.login(user_with_incorrect_email)

    assert non_authorized_user.status_code == 401
    assert non_authorized_user.json()["error"]["message"] == "Invalid email or password"


def test_user_can_make_deposit(balance_api, user_credential, bearer_token):
    make_deposit = balance_api.deposit(auth=bearer_token, asset="USDT", amount="1")
    assert make_deposit.status_code == 200

    user_assets = balance_api.get(auth=bearer_token)
    usdt_balance = next(b for b in user_assets.json() if b["asset"] == "USDT")

    assert Decimal(usdt_balance["available"]) == Decimal("1")


def test_deposit_without_token(balance_api, user_credential):
    make_deposit = balance_api.deposit(asset="USDT", amount="1")

    assert make_deposit.status_code == 401

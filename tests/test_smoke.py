import pytest


@pytest.mark.smoke
def test_health(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_registration(api_client, user_credential):
    response = api_client.post("/auth/register", json=user_credential)

    assert response.status_code == 201
    assert response.json()["email"] == user_credential["email"]
    assert "id" in response.json()


def test_register_with_the_same_creds(api_client, user_credential):
    api_client.post("/auth/register", json=user_credential)

    response = api_client.post("/auth/register", json=user_credential)
    assert response.status_code == 409
    assert response.json()["error"]["message"] == "User with this email already exists"


def test_login_auth(api_client, user_credential):
    api_client.post("/auth/register", json=user_credential)

    authorised_user = api_client.post("auth/login", json=user_credential)

    assert authorised_user.status_code == 200
    assert "access_token" in authorised_user.json()


def test_me_without_token(api_client):
    me = api_client.get("/me")
    assert me.status_code == 401


def test_me(api_client, user_credential, auth_token):
    me = api_client.get("/me", headers={"Authorization": f"Bearer {auth_token}"})
    assert me.status_code == 200


def test_login_with_incorrect_email(api_client, user_credential):
    response = api_client.post(
        "/auth/register", json={"email": user_credential["email"], "password": "sadas21312asd"}
    )

    assert response.status_code == 200

    authorised_user = api_client.post("auth/login", json=user_credential)

    assert authorised_user.status_code == 401


def test_user_can_make_deposit(api_client, user_credential, auth_token):
    make_deposit = api_client.post(
        "/balances/deposit",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"asset": "USDT", "amount": 1},
    )
    assert make_deposit.status_code == 200

    user_assets = api_client.get("/balances", headers={"Authorization": f"Bearer {auth_token}"})
    available_usdt = user_assets.json()[2]["available"]

    assert available_usdt == "1"

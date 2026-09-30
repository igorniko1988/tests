import uuid

from pytest import fixture

from framework.client import ApiClient


@fixture
def api_client():
    with ApiClient("http://localhost:8080") as client:
        yield client


@fixture
def user_credential():
    uid = uuid.uuid4().hex[:8]
    return {
        "email": f"qa+{uid}@example.com",
        "password": f"Aa1!{uuid.uuid4().hex[:12]}",
    }


@fixture
def auth_token(api_client, user_credential):
    response = api_client.post("/auth/register", json=user_credential)

    assert response.status_code == 201

    authorised_user = api_client.post("/auth/login", json=user_credential)

    assert authorised_user.status_code == 200
    assert "access_token" in authorised_user.json()
    token = authorised_user.json()["access_token"]
    return token

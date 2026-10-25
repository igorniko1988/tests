import pytest
from framework.models.auth import User


def test_me_returns_current_user(auth_api, credentials):
    r = auth_api.auth.me()

    assert r.status_code == 200
    User.model_validate(r.json())
    assert r.json()['email'] == credentials['email']


@pytest.mark.parametrize('email, password, message',(
        ('aslkdjsa@gmail.com','a3123','String should have at least 8 characters'),
        ('123213','asdasdasd','value is not a valid email address: An email address must have an @-sign.')
))
def test_register_with_invalid_creds(api, email, password,message):
    register = api.auth.register(email=email, password=password)

    assert register.status_code == 422
    assert register.json()['error']['details'][0]['message'] == message

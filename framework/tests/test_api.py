import pytest
from framework.models.balance import Balance
from framework.models.auth import User
from framework.models.order import Order


def test_me_returns_current_user(auth_api, credentials):
    r = auth_api.auth.me()
    User.model_validate(r.json())
    assert r.status_code == 200
    assert r.json()['email'] == credentials['email']


@pytest.mark.parametrize('email, password, message',(
        ('aslkdjsa@gmail.com','a3123','String should have at least 8 characters'),
        ('123213','asdasdasd','value is not a valid email address: An email address must have an @-sign.')
))
def test_register_with_invalid_creds(api, email, password,message):
    register = api.auth.register(email=email, password=password)
    assert register.status_code == 422
    assert register.json()['error']['details'][0]['message'] == message


def test_get_balances(auth_api):
    balances = auth_api.balances.get_balance()
    balance = [Balance.model_validate(b) for b in balances.json()]
    assert balances.status_code == 200


def test_deposit(auth_api):
    deposit = auth_api.balances.deposit('ETH','1')
    assert deposit.status_code == 200


def test_create_order(auth_api):
    auth_api.balances.deposit('USDT',100)
    order = auth_api.orders.create('ETH-USDT','BUY',"LIMIT",1,1)
    print(order.json())
    Order.model_validate(order)
    assert order.status_code == 201
from framework.models.balance import Balance


def test_get_balances(auth_api):
    balances = auth_api.balances.get_balance()

    assert balances.status_code == 200
    balance = [Balance.model_validate(b) for b in balances.json()]


def test_deposit(auth_api):
    deposit = auth_api.balances.deposit('ETH','1')

    assert deposit.status_code == 200

from framework.api.models.balance import Balance


def test_get_balances(auth_api):
    balances = auth_api.balances.get_balance()

    assert balances.status_code == 200
    for b in balances.json():
        Balance.model_validate(b)


def test_deposit(auth_api):
    deposit = auth_api.balances.deposit('ETH','1')

    assert deposit.status_code == 200

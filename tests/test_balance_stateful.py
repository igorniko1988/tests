"""Stateful-тест: Hypothesis сам придумывает последовательности действий
(депозиты, ордера, отмены) и после каждого шага проверяет инварианты баланса."""

from decimal import Decimal

from hypothesis import settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, precondition, rule

from framework.config import load_settings
from framework.factories.users import create_user
from framework.models.order import Order

money = st.decimals(min_value=Decimal("0.01"), max_value=Decimal("100"), places=2)


class BalanceMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        config = load_settings()
        self.user = create_user(config.base_url, config.timeout)
        # Наша «модель»: сколько денег ДОЛЖНО быть по нашим расчётам
        self.available = Decimal(0)
        self.locked = Decimal(0)
        self.open_orders: dict = {}  # id ордера -> сколько USDT он заблокировал

    @rule(amount=money)
    def deposit(self, amount):
        response = self.user.balances.deposit("USDT", str(amount))
        assert response.status_code == 200
        self.available += amount

    @rule(price=money, quantity=st.decimals(min_value=1, max_value=5, places=0))
    def place_buy_order(self, price, quantity):
        cost = price * quantity
        response = self.user.orders.create_order("ETH-USDT", "BUY", str(price), str(quantity))

        if cost > self.available:
            assert response.status_code == 400  # денег не хватает — должен отказать
        else:
            assert response.status_code == 201
            order = Order.model_validate(response.json())
            self.open_orders[order.id] = cost
            self.available -= cost
            self.locked += cost

    @precondition(lambda self: self.open_orders)
    @rule(data=st.data())
    def cancel_order(self, data):
        order_id = data.draw(st.sampled_from(sorted(self.open_orders)))
        response = self.user.orders.cancel_order(order_id)
        assert response.status_code == 200
        cost = self.open_orders.pop(order_id)
        self.available += cost
        self.locked -= cost

    @invariant()
    def balance_matches_model(self):
        usdt = self.user.get_balance("USDT")
        assert usdt.available >= 0
        assert usdt.locked >= 0
        assert usdt.available == self.available
        assert usdt.locked == self.locked

    def teardown(self):
        self.user.cancel_open_orders()
        self.user.client.close()


BalanceMachine.TestCase.settings = settings(max_examples=10, stateful_step_count=10, deadline=None)
TestBalanceStateful = BalanceMachine.TestCase

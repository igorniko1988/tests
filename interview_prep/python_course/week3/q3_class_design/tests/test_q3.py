import importlib
import inspect
import os
import time
from decimal import Decimal
from types import SimpleNamespace

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 и t06 ★: одни и те же тесты LRU ----------
LRU_MODULES = ["t01_lru_cache", pytest.param("t06_lru_by_hand", id="t06_lru_by_hand")]


@pytest.mark.parametrize("module", LRU_MODULES)
def test_t01_t06_lru_example(module):
    c = load(module).LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)
    assert c.keys() == ["a", "c"] and c.get("b") is None and c.get("b", 0) == 0
    assert len(c) == 2 and "a" in c and "b" not in c


@pytest.mark.parametrize("module", LRU_MODULES)
def test_t01_t06_lru_update_and_contains(module):
    c = load(module).LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)
    assert c.keys() == ["a", "c"] and c.get("a") == 10
    assert "c" in c
    c.put("d", 4)
    assert c.keys() == ["a", "d"], "проверка in не должна обновлять свежесть"
    with pytest.raises(ValueError):
        load(module).LRUCache(0)


@pytest.mark.parametrize("module", LRU_MODULES)
def test_t01_t06_lru_fast(module):
    c = load(module).LRUCache(1000)
    start = time.perf_counter()
    for i in range(100_000):
        c.put(i, i)
        c.get(i - 500)
    assert len(c) == 1000
    assert time.perf_counter() - start < 1.5, "get/put должны быть O(1)"


def test_t06_no_ordered_dict():
    module = load("t06_lru_by_hand")
    assert not hasattr(module, "OrderedDict") and "OrderedDict" not in inspect.getsource(module.LRUCache)


# ---------- t02 ----------
class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def test_t02_rate_limiter():
    clock = Clock()
    rl = load("t02_rate_limiter").RateLimiter(2, 10, clock)
    assert [rl.allow(), rl.allow(), rl.allow()] == [True, True, False]
    assert rl.remaining() == 0 and rl.retry_after() == 10
    clock.now = 4
    assert rl.retry_after() == 6 and rl.allow() is False
    clock.now = 10
    assert rl.remaining() == 2 and rl.allow() is True


def test_t02_sliding_not_fixed():
    clock = Clock()
    rl = load("t02_rate_limiter").RateLimiter(2, 10, clock)
    clock.now = 9
    assert rl.allow() and rl.allow()
    clock.now = 11  # фиксированное окно уже сбросилось бы
    assert rl.allow() is False
    clock.now = 19
    assert rl.allow() is True


def test_t02_validation():
    RateLimiter = load("t02_rate_limiter").RateLimiter
    for args in [(0, 10), (1, 0), (1, -1)]:
        with pytest.raises(ValueError):
            RateLimiter(*args, clock=Clock())


# ---------- t03 ----------
def test_t03_account_flow():
    module = load("t03_bank_account")
    acc = module.Account("ann")
    acc.deposit("100")
    acc.withdraw(30)
    assert acc.balance == Decimal("70.00") and str(acc.balance) == "70.00"
    with pytest.raises(module.InsufficientFunds) as error:
        acc.withdraw(100)
    assert error.value.balance == Decimal("70.00") and error.value.amount == Decimal("100")
    assert isinstance(error.value, module.BankError)
    assert acc.history == [("deposit", Decimal("100")), ("withdraw", Decimal("30"))]
    acc.history.append(("hack", 1))
    assert len(acc.history) == 2


def test_t03_validation_and_close():
    module = load("t03_bank_account")
    acc = module.Account("bob")
    with pytest.raises(TypeError):
        acc.deposit(1.5)
    with pytest.raises(ValueError):
        acc.deposit(0)
    acc.deposit(5)
    with pytest.raises(module.BankError):
        acc.close()
    acc.withdraw(5)
    acc.close()
    with pytest.raises(module.AccountClosed):
        acc.deposit(1)
    with pytest.raises(AttributeError):
        acc.balance = Decimal("1")


# ---------- t04 ----------
def test_t04_money_ops():
    Money = load("t04_money").Money
    a = Money("10.5", "usd")
    assert str(a) == "10.50 USD" and repr(a) == "Money('10.50', 'USD')"
    assert a + Money(2, "USD") == Money("12.50", "USD")
    assert a - Money("0.5", "USD") == Money(10, "USD")
    assert a * 2 == Money(21, "USD") and 3 * Money("0.10", "USD") == Money("0.30", "USD")
    assert Money("10", "USD") * Decimal("0.333") == Money("3.33", "USD")
    assert sum([Money(1, "USD"), Money(2, "USD")], Money.zero("usd")) == Money(3, "USD")


def test_t04_money_compare_hash():
    Money = load("t04_money").Money
    assert Money("1", "USD") != Money("1", "EUR")
    assert len({Money("1.00", "USD"), Money(1, "usd"), Money(1, "EUR")}) == 2
    assert Money(1, "USD") < Money(2, "USD") and Money(2, "USD") >= Money(2, "USD")
    with pytest.raises(ValueError):
        Money(1, "USD") < Money(2, "EUR")
    with pytest.raises(ValueError):
        Money(1, "USD") + Money(1, "EUR")


def test_t04_money_immutable_and_validation():
    Money = load("t04_money").Money
    m = Money(1, "USD")
    with pytest.raises(AttributeError):
        m.amount = Decimal("5")
    with pytest.raises(TypeError):
        Money(1.5, "USD")
    with pytest.raises(ValueError):
        Money(1, "US")


# ---------- t05 ★ ----------
class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        status, body = self.responses.pop(0)
        return SimpleNamespace(status=status, body=body)


def test_t05_api_client():
    module = load("t05_api_client")
    session = FakeSession([(200, {"access_token": "tok"}), (200, [1, 2]), (201, {"id": 5})])
    client = module.ApiClient("http://api/", session)
    assert client.login("a@b.io", "pw") == "tok"
    assert client.get("/orders", status="NEW") == [1, 2]
    assert client.post("/orders", {"qty": 1}) == {"id": 5}
    assert session.calls == [
        ("POST", "http://api/auth/login", {"headers": {"Accept": "application/json"}, "json": {"email": "a@b.io", "password": "pw"}}),
        ("GET", "http://api/orders", {"headers": {"Accept": "application/json", "Authorization": "Bearer tok"}, "params": {"status": "NEW"}}),
        ("POST", "http://api/orders", {"headers": {"Accept": "application/json", "Authorization": "Bearer tok"}, "json": {"qty": 1}}),
    ]


def test_t05_api_error():
    module = load("t05_api_client")
    client = module.ApiClient("http://api", FakeSession([(422, {"detail": "bad qty"})]), token="t")
    with pytest.raises(module.ApiError) as error:
        client.post("/orders", {"qty": 0})
    assert error.value.status == 422 and error.value.body == {"detail": "bad qty"}
    assert str(error.value) == "HTTP 422: {'detail': 'bad qty'}"

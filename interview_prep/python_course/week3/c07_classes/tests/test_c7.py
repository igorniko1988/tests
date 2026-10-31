import importlib
import os
from decimal import Decimal

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 ----------
def test_t01_user_normalizes():
    User = load("t01_user").User
    u = User(" Ann ", " Ann@Mail.COM ")
    assert (u.name, u.email, u.domain) == ("Ann", "ann@mail.com", "mail.com")
    u.email = "x@y.io"
    assert u.domain == "y.io"


@pytest.mark.parametrize("email", ["bob@mail", "bobmail.com", "@mail.com", "a@@b.com", "a@b@c.com", "a@.com", ""])
def test_t01_invalid_email(email):
    with pytest.raises(ValueError):
        load("t01_user").User("Bob", email)


def test_t01_setter_validates_and_domain_read_only():
    u = load("t01_user").User("Ann", "a@b.io")
    with pytest.raises(ValueError):
        u.email = "bad"
    assert u.email == "a@b.io"
    with pytest.raises(AttributeError):
        u.domain = "x.io"


def test_t01_empty_name():
    with pytest.raises(ValueError):
        load("t01_user").User("  ", "a@b.io")


# ---------- t02 ----------
DATA = {"id": "17", "symbol": "BTC/USDT", "side": "buy", "qty": "2", "price": "10.50"}


def test_t02_from_json():
    o = load("t02_order_from_json").Order.from_json(DATA)
    assert (o.order_id, o.symbol, o.side, o.qty) == (17, "BTC/USDT", "BUY", 2)
    assert o.price == Decimal("10.50") and isinstance(o.price, Decimal)
    assert o.total == Decimal("21.00")


def test_t02_subclass():
    Order = load("t02_order_from_json").Order

    class LimitOrder(Order):
        pass

    assert type(LimitOrder.from_json(DATA)) is LimitOrder


def test_t02_errors():
    Order = load("t02_order_from_json").Order
    with pytest.raises(ValueError):
        Order.from_json({**DATA, "side": "hold"})
    with pytest.raises(KeyError):
        Order.from_json({k: v for k, v in DATA.items() if k != "price"})


# ---------- t03 ----------
def test_t03_counters():
    Session = load("t03_session_counter").Session
    Session.reset_counters()
    a, b = Session(), Session()
    assert (a.number, b.number) == (1, 2)
    assert not a.closed
    a.close()
    a.close()
    assert a.closed
    assert (Session.created, Session.active) == (2, 1)
    c = Session()
    assert c.number == 3 and (Session.created, Session.active) == (3, 2)
    Session.reset_counters()
    assert (Session.created, Session.active) == (0, 0)
    assert "created" not in vars(a), "счётчик должен жить в классе, а не в объекте"


# ---------- t04 ----------
def test_t04_logs_are_independent():
    RequestLog = load("t04_find_the_bug").RequestLog
    a, b = RequestLog("a"), RequestLog("b")
    a.add("GET", "/orders")
    assert b.entries == []
    b.add("POST", "/orders")
    b.clear()
    assert a.entries == ["GET /orders"]
    assert RequestLog("c").entries == []
    assert a.name == "a"


# ---------- t05 ----------
def test_t05_money():
    Money = load("t05_money").Money
    m = Money("10.5", "usd")
    assert (m.amount, m.currency, m.formatted) == (Decimal("10.50"), "USD", "10.50 USD")
    total = m.add(Money(2, "USD"))
    assert total.formatted == "12.50 USD" and m.formatted == "10.50 USD"
    assert Money(Decimal("0.125"), "EUR").amount == Decimal("0.13")


def test_t05_read_only_and_validation():
    Money = load("t05_money").Money
    m = Money("1", "USD")
    with pytest.raises(AttributeError):
        m.amount = Decimal("5")
    with pytest.raises(AttributeError):
        m.currency = "EUR"
    with pytest.raises(TypeError):
        Money(1.5, "USD")
    for bad in ("US", "usdx", "12$"):
        with pytest.raises(ValueError):
            Money("1", bad)
    with pytest.raises(ValueError):
        m.add(Money("1", "EUR"))


# ---------- t06 ★ ----------
def test_t06_lazy_property():
    lazy_property = load("t06_lazy_property").lazy_property
    calls = []

    class Report:
        def __init__(self, rows):
            self.rows = rows

        @lazy_property
        def total(self):
            calls.append(1)
            return sum(self.rows)

    a, b = Report([1, 2]), Report([10])
    assert (a.total, a.total, b.total) == (3, 3, 10)
    assert len(calls) == 2
    a.rows.append(5)
    assert a.total == 3
    del a.total
    assert a.total == 8 and len(calls) == 3
    assert isinstance(Report.total, lazy_property)


def test_t06_not_functools():
    import inspect

    source = inspect.getsource(load("t06_lazy_property").lazy_property)
    assert "cached_property" not in source

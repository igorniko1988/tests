import dataclasses
import importlib
import os
from decimal import Decimal

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 ----------
def test_t01_vector_ops():
    V = load("t01_vector").Vector
    assert V(1, 2) + V(3, 4) == V(4, 6)
    assert V(5, 5) - V(1, 2) == V(4, 3)
    assert V(1, 2) * 3 == V(3, 6) and 2 * V(1, 2) == V(2, 4)
    assert abs(V(3, 4)) == 5.0
    assert repr(V(1, 2)) == "Vector(1, 2)"
    assert sum([V(1, 1), V(2, 2)]) == V(3, 3)


def test_t01_vector_eq_and_hash():
    V = load("t01_vector").Vector
    assert (V(1, 2) == (1, 2)) is False
    assert V(1, 2) != V(2, 1)
    assert len({V(1, 2), V(1, 2), V(0, 0)}) == 2
    a = V(1, 1)
    a + V(1, 1)
    assert a == V(1, 1), "операции не должны менять исходный вектор"


# ---------- t02 ----------
def test_t02_cart():
    cart = load("t02_cart").Cart()
    assert not cart and len(cart) == 0
    cart.add("apple", 2)
    cart.add("pear")
    cart.add("apple")
    assert len(cart) == 2 and cart["apple"] == 3 and "pear" in cart and "kiwi" not in cart
    assert cart.total_qty == 4 and bool(cart)
    assert list(cart) == [("apple", 3), ("pear", 1)]
    cart.remove("apple")
    assert list(cart) == [("pear", 1)]


def test_t02_cart_errors():
    cart = load("t02_cart").Cart()
    with pytest.raises(KeyError):
        cart["kiwi"]
    with pytest.raises(KeyError):
        cart.remove("kiwi")
    with pytest.raises(ValueError):
        cart.add("apple", 0)


# ---------- t03 ----------
def test_t03_sorting_and_compare():
    Version = load("t03_version").Version
    assert sorted(["1.10.0", "1.9.3", "1.2"], key=Version) == ["1.2", "1.9.3", "1.10.0"]
    assert Version("1.10") > Version("1.9")
    assert Version("2.0") >= Version("1.10") and Version("1.2") <= Version("1.2.0")
    assert Version("1.2") == Version("1.2.0") and Version("1.2") != Version("1.2.1")


def test_t03_hash_str_repr():
    Version = load("t03_version").Version
    assert len({Version("1.2"), Version("1.2.0"), Version("1.3")}) == 2
    assert str(Version("1.10.0")) == "1.10.0" and repr(Version("1.10.0")) == "Version('1.10.0')"


@pytest.mark.parametrize("text", ["1.x", "", "1..2", "v1"])
def test_t03_invalid(text):
    with pytest.raises(ValueError):
        load("t03_version").Version(text)


# ---------- t04 ----------
def test_t04_order_dataclass():
    Order = load("t04_order_dataclass").Order
    assert dataclasses.is_dataclass(Order)
    assert [f.name for f in dataclasses.fields(Order)] == ["symbol", "side", "qty", "price", "tags"]
    o = Order("BTC", "buy", qty=2, price="10.50")
    assert o.side == "BUY" and o.price == Decimal("10.50") and isinstance(o.price, Decimal)
    assert Order("ETH", "sell") == Order("ETH", "SELL")
    a, b = Order("BTC", "BUY"), Order("BTC", "BUY")
    a.tags.append("smoke")
    assert b.tags == []
    assert o.to_payload() == {"symbol": "BTC", "side": "BUY", "qty": 2, "price": "10.50", "tags": []}


def test_t04_validation():
    Order = load("t04_order_dataclass").Order
    with pytest.raises(ValueError):
        Order("BTC", "hold")
    with pytest.raises(ValueError):
        Order("BTC", "buy", qty=0)
    with pytest.raises(TypeError):
        Order("BTC", "buy", price=10.5)
    assert Order("BTC", "buy", price=7).price == Decimal("7")


# ---------- t05 ----------
def test_t05_ticker():
    Ticker = load("t05_hashable_ticker").Ticker
    assert Ticker(" btc ", "Binance") == Ticker("BTC", "binance")
    assert len({Ticker("btc", "binance"), Ticker("BTC", "Binance"), Ticker("ETH", "binance")}) == 2
    prices = {Ticker("BTC", "binance"): 100}
    assert prices[Ticker(" btc", "BINANCE")] == 100
    assert repr(Ticker("btc", "binance")) == "Ticker('BTC', 'BINANCE')"
    assert (Ticker("BTC", "X") == "BTC") is False


def test_t05_read_only():
    t = load("t05_hashable_ticker").Ticker("BTC", "X")
    with pytest.raises(AttributeError):
        t.symbol = "ETH"
    with pytest.raises(AttributeError):
        t.exchange = "Y"


# ---------- t06 ★ ----------
def test_t06_recorder():
    r = load("t06_recorder").Recorder()
    r.returns["api.get_user"] = {"id": 7}
    assert r.api.get_user(7) == {"id": 7}
    assert r.log.info("done") is None
    r.client.orders.create(symbol="BTC")
    r()
    assert r.calls == [
        ("api.get_user", (7,), {}),
        ("log.info", ("done",), {}),
        ("client.orders.create", (), {"symbol": "BTC"}),
        ("", (), {}),
    ]
    assert isinstance(r.calls, list) and isinstance(r.returns, dict)

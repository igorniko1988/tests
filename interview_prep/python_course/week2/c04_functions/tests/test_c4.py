import importlib
import os
import time
from functools import partial

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 ----------
def test_t01_default_counter():
    c = load("t01_make_counter").make_counter()
    assert [c(), c(), c()] == [0, 1, 2]


def test_t01_counters_are_independent():
    make_counter = load("t01_make_counter").make_counter
    c, d = make_counter(), make_counter(10, 5)
    assert [c(), d(), d(), c()] == [0, 10, 15, 1]


def test_t01_negative_step():
    c = load("t01_make_counter").make_counter(3, -1)
    assert [c(), c(), c(), c()] == [3, 2, 1, 0]


def test_t01_uses_closure():
    c = load("t01_make_counter").make_counter()
    assert c.__closure__, "счётчик должен хранить состояние в замыкании"


# ---------- t02 ----------
def test_t02_example():
    log = []

    def add(a, b, c=0):
        return a + b + c

    logged = load("t02_call_logger").call_logger(add, log)
    assert logged(1, 2, c=3) == 6
    assert log == ["add(1, 2, c=3) -> 6"]


def test_t02_repr_and_no_args():
    log = []

    def greet(name):
        return f"Hello, {name}"

    def ping():
        return None

    call_logger = load("t02_call_logger").call_logger
    call_logger(greet, log)("Ann")
    call_logger(ping, log)()
    assert log == ["greet('Ann') -> 'Hello, Ann'", "ping() -> None"]


def test_t02_exception_is_not_logged():
    log = []

    def boom():
        raise ValueError("x")

    with pytest.raises(ValueError):
        load("t02_call_logger").call_logger(boom, log)()
    assert log == []


def test_t02_kwargs_only():
    log = []

    def make(**fields):
        return len(fields)

    load("t02_call_logger").call_logger(make, log)(a=1, b="x")
    assert log == ["make(a=1, b='x') -> 2"]


# ---------- t03 ----------
@pytest.mark.parametrize(("n", "expected"), [(3, [0, 10, 20]), (0, []), (1, [0]), (5, [0, 10, 20, 30, 40])])
def test_t03_make_multipliers(n, expected):
    assert [f(10) for f in load("t03_make_multipliers").make_multipliers(n)] == expected


# ---------- t04 ----------
USERS = [
    {"name": "bob", "age": 30},
    {"name": "ann", "age": 25},
    {"name": "cat", "age": 30},
]


def names(records):
    return [r["name"] for r in records]


@pytest.mark.parametrize(
    ("fields", "expected"),
    [
        (("age",), ["ann", "bob", "cat"]),
        (("-age", "name"), ["bob", "cat", "ann"]),
        (("-age", "-name"), ["cat", "bob", "ann"]),
        (("-name",), ["cat", "bob", "ann"]),
        ((), ["bob", "ann", "cat"]),
    ],
)
def test_t04_sort_by(fields, expected):
    users = [dict(u) for u in USERS]
    result = load("t04_sort_by").sort_by(users, *fields)
    assert names(result) == expected
    assert names(users) == ["bob", "ann", "cat"], "исходный список не должен меняться"
    assert result is not users


# ---------- t05 ----------
def fake_request(method, resource, item_id=None, *, timeout=5, **body):
    return (method, resource, item_id, timeout, body)


def test_t05_helpers():
    client = load("t05_build_client").build_client(fake_request)
    assert client["get_user"](7) == ("GET", "users", 7, 5, {})
    assert client["get_order"](3) == ("GET", "orders", 3, 5, {})
    assert client["create_order"](symbol="BTC", qty=2) == ("POST", "orders", None, 10, {"symbol": "BTC", "qty": 2})
    assert client["health"]() == ("GET", "health", None, 1, {})


def test_t05_uses_partial():
    client = load("t05_build_client").build_client(fake_request)
    assert set(client) == {"get_user", "get_order", "create_order", "health"}
    assert all(isinstance(f, partial) for f in client.values()), "каждый помощник — functools.partial"


# ---------- t06 ★ ----------
def test_t06_fib_fast_and_counted():
    memoize = load("t06_memoize").memoize

    @memoize
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    start = time.perf_counter()
    assert fib(100) == 354224848179261915075
    assert time.perf_counter() - start < 0.5
    assert fib.calls == 101


def test_t06_kwargs_order_does_not_matter():
    memoize = load("t06_memoize").memoize
    seen = []

    @memoize
    def f(a, b=0):
        seen.append((a, b))
        return a + b

    assert f(1, b=2) == 3
    assert f(1, b=2) == 3
    assert f(a=1, b=2) == 3
    assert f(b=2, a=1) == 3
    assert f.calls == 2  # (1, b=2) и (a=1, b=2) — разные ключи, порядок kwargs не важен
    assert len(seen) == 2


def test_t06_no_functools_cache():
    import inspect

    module = load("t06_memoize")
    source = inspect.getsource(module.memoize)
    assert "cache(" not in source and not hasattr(module, "lru_cache") and not hasattr(module, "cache"), (
        "кэш нужно написать самому, без functools"
    )

import copy
import importlib
import os

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 ★ ----------
def test_t01_example():
    lines = [
        "GET /orders 200 15ms",
        "POST /orders 503 120ms",
        "GET /health 200 1ms",
        "broken line",
        "GET /orders 500 30ms",
    ]
    result = load("t01_endpoint_stats").endpoint_stats(lines)
    assert result == {"/orders": {"count": 3, "errors": 2}, "/health": {"count": 1, "errors": 0}}
    assert list(result) == ["/orders", "/health"]


@pytest.mark.parametrize(
    ("lines", "expected"),
    [
        ([], {}),
        (["GET /a abc 1ms", "GET /a 404 1ms extra", ""], {}),
        (["GET /a 404 1ms", "GET /a 499 1ms"], {"/a": {"count": 2, "errors": 0}}),
    ],
)
def test_t01_edge_cases(lines, expected):
    assert load("t01_endpoint_stats").endpoint_stats(lines) == expected


# ---------- t02 ----------
def test_t02_example():
    old = {"id": 1, "status": "NEW", "price": "10.00"}
    new = {"id": 1, "status": "FILLED", "qty": 2}
    assert load("t02_json_diff").json_diff(old, new) == {
        "added": ["qty"],
        "removed": ["price"],
        "changed": ["status"],
    }


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        ({}, {}, {"added": [], "removed": [], "changed": []}),
        ({"a": 1}, {"a": 1}, {"added": [], "removed": [], "changed": []}),
        ({"b": 1, "a": 2}, {}, {"added": [], "removed": ["a", "b"], "changed": []}),
        ({"a": [1]}, {"a": [1, 2], "c": None, "b": 0}, {"added": ["b", "c"], "removed": [], "changed": ["a"]}),
        ({"a": 1}, {"a": 1.0}, {"added": [], "removed": [], "changed": []}),
    ],
)
def test_t02_cases(old, new, expected):
    assert load("t02_json_diff").json_diff(old, new) == expected


# ---------- t03 ----------
def test_t03_example():
    users = [
        {"id": 1, "email": "Ann@Mail.com"},
        {"id": 2, "email": "bob@mail.com"},
        {"id": 3, "email": " ann@mail.com "},
        {"id": 4, "email": "BOB@MAIL.COM"},
        {"id": 5, "email": "cat@mail.com"},
    ]
    assert load("t03_duplicate_emails").duplicate_emails(users) == ["ann@mail.com", "bob@mail.com"]


@pytest.mark.parametrize(
    ("emails", "expected"),
    [
        ([], []),
        (["a@x.io"], []),
        (["a@x.io", "A@X.IO", "a@x.io"], ["a@x.io"]),
        (["b@x.io", "a@x.io", "a@x.io", "b@x.io"], ["b@x.io", "a@x.io"]),
    ],
)
def test_t03_cases(emails, expected):
    users = [{"id": i, "email": e} for i, e in enumerate(emails)]
    assert load("t03_duplicate_emails").duplicate_emails(users) == expected


# ---------- t04 ----------
def test_t04_example():
    orders = [
        {"id": 1, "status": "NEW", "amount": "10.10"},
        {"id": 2, "status": "FILLED", "amount": "5"},
        {"id": 3, "status": "NEW", "amount": "0.2"},
    ]
    result = load("t04_orders_summary").orders_summary(orders)
    assert result == {"NEW": {"count": 2, "total": "10.30"}, "FILLED": {"count": 1, "total": "5.00"}}
    assert list(result) == ["NEW", "FILLED"]


@pytest.mark.parametrize(
    ("amounts", "total"),
    [
        (["0.1", "0.2"], "0.30"),
        (["0.125"], "0.13"),
        (["0.005", "0.005"], "0.01"),
        (["100", "-0.5"], "99.50"),
    ],
)
def test_t04_decimal_rounding(amounts, total):
    orders = [{"id": i, "status": "NEW", "amount": a} for i, a in enumerate(amounts)]
    result = load("t04_orders_summary").orders_summary(orders)
    assert result == {"NEW": {"count": len(amounts), "total": total}}


def test_t04_empty():
    assert load("t04_orders_summary").orders_summary([]) == {}


# ---------- t05 ----------
@pytest.mark.parametrize(
    ("data", "sep", "expected"),
    [
        ({"a": 1, "b": {"c": 2, "d": {"e": 3}}}, ".", {"a": 1, "b.c": 2, "b.d.e": 3}),
        ({"user": {"tags": ["x"]}}, "/", {"user/tags": ["x"]}),
        ({}, ".", {}),
        ({"a": {}}, ".", {"a": {}}),
        ({"a": {"b": None}, "c": [{"d": 1}]}, ".", {"a.b": None, "c": [{"d": 1}]}),
    ],
)
def test_t05_flatten(data, sep, expected):
    result = load("t05_flatten").flatten(data, sep=sep)
    assert result == expected
    assert list(result) == list(expected)


def test_t05_default_sep_and_input_untouched():
    data = {"a": {"b": {"c": 1}}}
    before = copy.deepcopy(data)
    assert load("t05_flatten").flatten(data) == {"a.b.c": 1}
    assert data == before


# ---------- t06 ★ ----------
@pytest.mark.parametrize(
    ("data", "schema", "expected"),
    [
        ({"id": 1, "symbol": "BTC"}, {"id": int, "symbol": str}, []),
        ({"id": "1"}, {"id": int, "symbol": str}, ["type: id expected int, got str", "missing: symbol"]),
        ({"id": True}, {"id": int}, ["type: id expected int, got bool"]),
        ({"price": None}, {"price": str}, ["type: price expected str, got NoneType"]),
        ({"id": 1, "extra": 2}, {"id": int}, []),
        ({}, {}, []),
    ],
)
def test_t06_validate(data, schema, expected):
    assert load("t06_validate").validate(data, schema) == expected

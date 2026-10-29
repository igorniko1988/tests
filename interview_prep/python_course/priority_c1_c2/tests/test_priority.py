import copy
import importlib
import inspect
from decimal import Decimal

import pytest



def load(name):
    return importlib.import_module(name)


# ---------- C1 t01 ----------
def test_c1_t01_calls_are_independent():
    add_tag = load("c1_t01_fix_default").add_tag
    assert add_tag("smoke") == ["smoke"]
    assert add_tag("api") == ["api"]


def test_c1_t01_own_list_is_mutated_and_returned():
    add_tag = load("c1_t01_fix_default").add_tag
    mine = ["ui"]
    result = add_tag("x", mine)
    assert result is mine
    assert mine == ["ui", "x"]


def test_c1_t01_empty_list_passed_is_used():
    add_tag = load("c1_t01_fix_default").add_tag
    mine = []
    assert add_tag("x", mine) is mine



# ---------- C1 t04 ----------
ORDER = {"symbol": "BTC/USDT", "side": "buy", "meta": {"tags": ["smoke"]}}


def test_c1_t04_changes_applied():
    template = copy.deepcopy(ORDER)
    p = load("c1_t04_build_payload").build_payload(template, side="sell", qty="0.1")
    assert p == {"symbol": "BTC/USDT", "side": "sell", "meta": {"tags": ["smoke"]}, "qty": "0.1"}
    assert template == ORDER


def test_c1_t04_template_untouched_after_nested_change():
    template = copy.deepcopy(ORDER)
    p = load("c1_t04_build_payload").build_payload(template)
    assert p is not template
    p["meta"]["tags"].append("x")
    assert template["meta"]["tags"] == ["smoke"]


def test_c1_t04_change_value_not_shared():
    template = {"items": []}
    tags = ["a"]
    p = load("c1_t04_build_payload").build_payload(template, tags=tags)
    p["tags"].append("b")
    assert tags == ["a"]



# ---------- C1 t07 ----------
@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([3, 1, 3, 2, 1], [3, 1, 2]),
        ([{"id": 1}, {"id": 2}, {"id": 1}], [{"id": 1}, {"id": 2}]),
        ([[1, 2], [1, 2], [2, 1]], [[1, 2], [2, 1]]),
        ([], []),
        (["a"], ["a"]),
        ([{"a": 1, "b": 2}, {"b": 2, "a": 1}], [{"a": 1, "b": 2}]),
    ],
)
def test_c1_t07_dedupe(items, expected):
    assert load("c1_t07_dedupe").dedupe(items) == expected


def test_c1_t07_returns_original_objects():
    first = {"id": 1}
    result = load("c1_t07_dedupe").dedupe([first, {"id": 1}])
    assert result[0] is first


def test_c1_t07_linear_enough():
    items = [{"id": i % 1000} for i in range(20000)]
    assert len(load("c1_t07_dedupe").dedupe(items)) == 1000



# ---------- C2 t01 ----------
@pytest.mark.parametrize(
    ("lines", "fee", "expected"),
    [
        ([("19.99", 3)], "0", "59.97"),
        ([("19.99", 3)], "0.1", "60.03"),
        ([("0.1", 3)], "0", "0.30"),
        ([("0.125", 1)], "0", "0.13"),
        ([("0.115", 1)], "0", "0.12"),
        ([], "0", "0.00"),
        ([("100", 1), ("0.01", 2)], "0", "100.02"),
        ([("1000", 1)], "0.15", "1001.50"),
    ],
)
def test_c2_t01_total(lines, fee, expected):
    assert load("c2_t01_order_total").order_total(lines, fee) == expected


def test_c2_t01_default_fee_and_type():
    result = load("c2_t01_order_total").order_total([("2.5", 2)])
    assert isinstance(result, str)
    assert result == "5.00"



# ---------- C2 t04 ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        ("А роза упала на лапу Азора", True),
        ("0P", False),
        ("", True),
        ("!!", True),
        ("ab_a", True),
        ("Ab", False),
        ("No 'x' in Nixon", True),
    ],
)
def test_c2_t04_palindrome(s, expected):
    assert load("c2_t04_is_palindrome").is_palindrome(s) is expected



# ---------- C2 t07 ----------
@pytest.mark.parametrize(
    ("args", "kwargs", "expected"),
    [
        ((None, 0, 5), {}, 0),
        ((None, "", "x"), {}, ""),
        ((None, None), {}, None),
        ((None,), {"default": 1}, 1),
        ((), {}, None),
        ((), {"default": "d"}, "d"),
        ((False, True), {}, False),
        ((None, []), {"default": 1}, []),
    ],
)
def test_c2_t07_coalesce(args, kwargs, expected):
    result = load("c2_t07_coalesce").coalesce(*args, **kwargs)
    assert result == expected
    assert type(result) is type(expected)

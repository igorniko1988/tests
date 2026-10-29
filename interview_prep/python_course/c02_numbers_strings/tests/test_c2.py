import importlib
import inspect
import os
from decimal import Decimal

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в папках разделов.
SRC = os.environ.get("SRC", "tasks")
SECTION = {
    "t01_order_total": "s03_decimal",
    "t02_parse_amount": "s03_decimal",
    "t03_round_half_up": "s03_decimal",
    "t04_is_palindrome": "s04_strings",
    "t05_format_report": "s05_fstrings",
    "t06_decode_body": "s06_bytes",
    "t07_coalesce": "s07_truthy",
}


def load(name):
    package = SECTION[name] if SRC == "tasks" else SRC
    return importlib.import_module(f"{package}.{name}")


# ---------- t01 ----------
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
def test_t01_total(lines, fee, expected):
    assert load("t01_order_total").order_total(lines, fee) == expected


def test_t01_default_fee_and_type():
    result = load("t01_order_total").order_total([("2.5", 2)])
    assert isinstance(result, str)
    assert result == "5.00"


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("12", "12"),
        (" 12.50 ", "12.50"),
        ("-3.1", "-3.1"),
        ("0", "0"),
        ("0.001", "0.001"),
    ],
)
def test_t02_valid(text, expected):
    result = load("t02_parse_amount").parse_amount(text)
    assert isinstance(result, Decimal)
    assert str(result) == expected


@pytest.mark.parametrize(
    "text",
    ["", "   ", "abc", "1,5", "+5", ".5", "5.", "1e3", "NaN", "nan", "Infinity", "-inf", "1.2.3", "--1", "١٢", None, 12, 1.5],
)
def test_t02_invalid(text):
    assert load("t02_parse_amount").parse_amount(text) is None


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("x", "digits", "expected"),
    [
        (2.675, 2, 2.68),
        (1.005, 2, 1.01),
        (2.5, 0, 3.0),
        (3.5, 0, 4.0),
        (-1.005, 2, -1.01),
        (-2.5, 0, -3.0),
        (1.004, 2, 1.0),
        (123.456, 1, 123.5),
        (0.125, 2, 0.13),
        (9.995, 2, 10.0),
        (0.0, 2, 0.0),
        (7.0, 3, 7.0),
        (0.0005, 3, 0.001),
    ],
)
def test_t03_round(x, digits, expected):
    assert load("t03_round_half_up").round_half_up(x, digits) == expected


def test_t03_default_digits():
    assert load("t03_round_half_up").round_half_up(2.675) == 2.68


def test_t03_no_decimal_module():
    source = inspect.getsource(load("t03_round_half_up"))
    assert "import decimal" not in source and "from decimal" not in source, "решение без модуля decimal"


# ---------- t04 ----------
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
def test_t04_palindrome(s, expected):
    assert load("t04_is_palindrome").is_palindrome(s) is expected


# ---------- t05 ----------
def test_t05_example():
    expected = "\n".join(
        [
            "Name     Amount",
            "---------------",
            "BTC    1,234.50",
            "ETH      100.00",
            "---------------",
            "Total  1,334.50",
        ]
    )
    assert load("t05_format_report").format_report([("BTC", "1234.5"), ("ETH", "99.999")]) == expected


def test_t05_empty():
    expected = "Name   Amount\n-------------\n-------------\nTotal    0.00"
    assert load("t05_format_report").format_report([]) == expected


def test_t05_long_name_and_big_total():
    report = load("t05_format_report").format_report([("TETHER_USD", "999999.99"), ("X", "0.01")])
    assert report.splitlines() == [
        "Name              Amount",
        "------------------------",
        "TETHER_USD    999,999.99",
        "X                   0.01",
        "------------------------",
        "Total       1,000,000.00",
    ]


def test_t05_no_trailing_newline():
    assert not load("t05_format_report").format_report([("A", "1")]).endswith("\n")


# ---------- t06 ----------
@pytest.mark.parametrize(
    ("data", "content_type", "expected"),
    [
        (b'{"a": 1}', None, '{"a": 1}'),
        ("привет".encode("cp1251"), "text/plain; charset=windows-1251", "привет"),
        ("привет".encode("utf-8"), "application/json; charset=utf-8", "привет"),
        (b"ok", 'text/html; Charset="UTF-8"', "ok"),
        ("ж".encode("cp1251"), "text/plain ;  charset = cp1251 ", "ж"),
        (b"ok", "text/plain; charset=no-such-codec", "ok"),
        (b"a\xffb", None, "a�b"),
        ("привет".encode("utf-8"), "application/json", "привет"),
        (b"", None, ""),
    ],
)
def test_t06_decode(data, content_type, expected):
    assert load("t06_decode_body").decode_body(data, content_type) == expected


def test_t06_default_argument():
    assert load("t06_decode_body").decode_body("€".encode()) == "€"


# ---------- t07 ----------
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
def test_t07_coalesce(args, kwargs, expected):
    result = load("t07_coalesce").coalesce(*args, **kwargs)
    assert result == expected
    assert type(result) is type(expected)

"""Тесты модуля 1. Одна задача: uv run pytest -k t03"""
import importlib
import inspect
import os

import pytest

SRC = os.environ.get("SRC", "tasks")   # SRC=solutions — проверить эталон


def load(module, name):
    return getattr(importlib.import_module(f"{SRC}.{module}"), name)


def body(module, name):
    """Код функции без строки def — для проверок «без sort», «без деления»."""
    src = inspect.getsource(load(module, name))
    assert "NotImplementedError" not in src, "задача ещё не решена"
    return src.split("\n", 1)[1]


@pytest.mark.parametrize("s,expected", [
    ("the sky is blue", "blue is sky the"),
    ("  hello   world  ", "world hello"),
    ("one", "one"),
    ("   ", ""),
    ("", ""),
])
def test_t01_reverse_words(s, expected):
    assert load("t01_reverse_words", "reverse_words")(s) == expected


@pytest.mark.parametrize("s,expected", [
    ("aaabcc", "a3b1c2"), ("abc", "a1b1c1"), ("aabaa", "a2b1a2"),
    ("", ""), ("z", "z1"), ("bbbbbbbbbbbb", "b12"),
])
def test_t02_compress(s, expected):
    assert load("t02_compress", "compress")(s) == expected


@pytest.mark.parametrize("nums,expected", [
    ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
    ([0], [0]), ([1, 2], [1, 2]), ([0, 0, 1], [1, 0, 0]), ([], []),
    ([4, 0, 5, 0, 0, 6], [4, 5, 6, 0, 0, 0]),
])
def test_t03_move_zeros(nums, expected):
    move_zeros = load("t03_move_zeros", "move_zeros")
    same = nums
    assert move_zeros(nums) is None
    assert nums is same and nums == expected


def test_t03_no_new_list():
    src = body("t03_move_zeros", "move_zeros")
    assert "[:]" not in src and "sorted" not in src and ".sort" not in src, \
        "нужно на месте за O(1) памяти"


@pytest.mark.parametrize("nums,k,expected", [
    ([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]),
    ([1, 2], 5, [2, 1]), ([1, 2, 3], 0, [1, 2, 3]), ([1, 2, 3], 3, [1, 2, 3]),
    ([], 3, []), ([-1, -100, 3, 99], 2, [3, 99, -1, -100]),
])
def test_t04_rotate(nums, k, expected):
    original = nums[:]
    assert load("t04_rotate", "rotate")(nums, k) == expected
    assert nums == original, "входной список менять нельзя"


@pytest.mark.parametrize("nums,expected", [
    ([3, 0, 1], 2), ([0, 1], 2), ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8), ([1], 0), ([0], 1),
])
def test_t05_missing_number(nums, expected):
    assert load("t05_missing_number", "missing_number")(nums) == expected


def test_t05_no_set_or_sort():
    src = body("t05_missing_number", "missing_number")
    assert "set(" not in src and "sort" not in src, "нужна память O(1)"


@pytest.mark.parametrize("digits,expected", [
    ([1, 2, 3], [1, 2, 4]), ([1, 2, 9], [1, 3, 0]), ([9, 9], [1, 0, 0]),
    ([0], [1]), ([9], [1, 0]), ([8, 9, 9, 9], [9, 0, 0, 0]),
])
def test_t06_plus_one(digits, expected):
    assert load("t06_plus_one", "plus_one")(digits) == expected


def test_t06_no_int_conversion():
    src = body("t06_plus_one", "plus_one")
    assert "int(" not in src and "str(" not in src, "без перевода в число"


@pytest.mark.parametrize("strs,expected", [
    (["flower", "flow", "flight"], "fl"), (["dog", "racecar", "car"], ""),
    (["alone"], "alone"), ([], ""), (["", "a"], ""), (["ab", "a"], "a"),
    (["same", "same"], "same"),
])
def test_t07_longest_common_prefix(strs, expected):
    assert load("t07_longest_common_prefix", "longest_common_prefix")(strs) == expected


@pytest.mark.parametrize("a,b,expected", [
    ([1, 3, 5], [2, 4, 6, 8], [1, 2, 3, 4, 5, 6, 8]), ([], [1], [1]), ([1], [], [1]),
    ([], [], []), ([1, 1], [1], [1, 1, 1]), ([5, 6], [1, 2], [1, 2, 5, 6]),
    ([-3, 0], [-5, -3, 10], [-5, -3, -3, 0, 10]),
])
def test_t08_merge_sorted(a, b, expected):
    assert load("t08_merge_sorted", "merge_sorted")(a, b) == expected


def test_t08_no_sort():
    src = body("t08_merge_sorted", "merge_sorted")
    assert "sort" not in src and "heapq" not in src, "нужно слияние за O(n + m)"


@pytest.mark.parametrize("prices,expected", [
    ([7, 1, 5, 3, 6, 4], 5), ([7, 6, 4, 3, 1], 0), ([], 0), ([5], 0),
    ([2, 4, 1], 2), ([3, 2, 6, 5, 0, 3], 4),
])
def test_t09_max_profit(prices, expected):
    assert load("t09_max_profit", "max_profit")(prices) == expected


def test_t09_linear_time():
    import time
    prices = list(range(20_000, 0, -1))
    t = time.perf_counter()
    load("t09_max_profit", "max_profit")(prices)
    assert time.perf_counter() - t < 0.5, "похоже на O(n^2), нужно O(n)"


@pytest.mark.parametrize("nums,expected", [
    ([1, 2, 3, 4], [24, 12, 8, 6]), ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
    ([2, 3], [3, 2]), ([0, 0], [0, 0]), ([5, 0, 2], [0, 10, 0]),
])
def test_t10_product_except_self(nums, expected):
    assert load("t10_product_except_self", "product_except_self")(nums) == expected


def test_t10_no_division():
    src = body("t10_product_except_self", "product_except_self")
    assert "/" not in src, "деление запрещено"

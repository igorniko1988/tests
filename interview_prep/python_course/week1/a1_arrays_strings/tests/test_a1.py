import importlib
import inspect
import os
import re
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")
TIME_LIMIT = 0.5  # секунды; O(n²) на этих размерах не укладывается


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("the sky is blue", "blue is sky the"),
        ("  hello   world  ", "world hello"),
        ("a", "a"),
        ("   ", ""),
        ("", ""),
    ],
)
def test_t01_reverse_words(s, expected):
    assert load("t01_reverse_words").reverse_words(s) == expected


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([1, 2], [1, 2]),
        ([], []),
        ([0, 0, 1], [1, 0, 0]),
    ],
)
def test_t02_move_zeros(nums, expected):
    assert load("t02_move_zeros").move_zeros(nums) is None
    assert nums == expected


def test_t02_same_list_object():
    nums = [0, 1]
    before = id(nums)
    load("t02_move_zeros").move_zeros(nums)
    assert id(nums) == before


def test_t02_linear():
    nums = [0, 1] * 50_000
    _, spent = timed(load("t02_move_zeros").move_zeros, nums)
    assert nums == [1] * 50_000 + [0] * 50_000
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([1, 3, 5], [2, 4], [1, 2, 3, 4, 5]),
        ([1, 1], [1], [1, 1, 1]),
        ([], [7], [7]),
        ([], [], []),
        ([1, 2, 3], [10, 20], [1, 2, 3, 10, 20]),
    ],
)
def test_t03_merge_sorted(a, b, expected):
    a_copy, b_copy = list(a), list(b)
    assert load("t03_merge_sorted").merge_sorted(a, b) == expected
    assert a == a_copy and b == b_copy


def test_t03_no_builtin_sort():
    source = inspect.getsource(load("t03_merge_sorted").merge_sorted)
    assert not re.search(r"\bsorted\(|\.sort\(", source), "sorted() и .sort() запрещены условием"


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("prices", "expected"),
    [
        ([7, 1, 5, 3, 6, 4], 5),
        ([7, 6, 4, 3, 1], 0),
        ([], 0),
        ([5], 0),
        ([2, 4, 1], 2),
        ([3, 8, 1, 4], 5),
    ],
)
def test_t04_max_profit(prices, expected):
    assert load("t04_max_profit").max_profit(prices) == expected


def test_t04_linear():
    prices = list(range(200_000, 0, -1))
    result, spent = timed(load("t04_max_profit").max_profit, prices)
    assert result == 0
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t05 ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([2, 0, 3], [0, 6, 0]),
        ([0, 0, 5], [0, 0, 0]),
        ([7], [1]),
        ([-1, 2, -3], [-6, 3, -2]),
    ],
)
def test_t05_product_except_self(nums, expected):
    assert load("t05_product_except_self").product_except_self(nums) == expected


def test_t05_no_division():
    source = inspect.getsource(load("t05_product_except_self").product_except_self)
    assert "/" not in source, "деление запрещено условием"


def test_t05_linear():
    nums = [1] * 100_000
    result, spent = timed(load("t05_product_except_self").product_except_self, nums)
    assert result == nums
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t06 ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("aaab", "a3b1"),
        ("aabcccccaa", "a2b1c5a2"),
        ("abc", "a1b1c1"),
        ("", ""),
        ("aA", "a1A1"),
        ("zzzzzzzzzzzz", "z12"),
    ],
)
def test_t06_compress(s, expected):
    assert load("t06_compress").compress(s) == expected


# ---------- t07 ★ ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([1, 2], 3, [2, 1]),
        ([], 5, []),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1, 2, 3], 3, [1, 2, 3]),
    ],
)
def test_t07_rotate(nums, k, expected):
    before = id(nums)
    assert load("t07_rotate").rotate(nums, k) is None
    assert nums == expected and id(nums) == before


# ---------- t08 ★ ----------
@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["flower", "flow", "flight"], "fl"),
        (["dog", "racecar", "car"], ""),
        (["alone"], "alone"),
        ([], ""),
        (["ab", "a"], "a"),
    ],
)
def test_t08_common_prefix(words, expected):
    assert load("t08_common_prefix").common_prefix(words) == expected


# ---------- t09 ★ ----------
@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [
        ("abc", "ahbgdc", True),
        ("axc", "ahbgdc", False),
        ("", "abc", True),
        ("aa", "a", False),
        ("ba", "ab", False),
    ],
)
def test_t09_is_subsequence(s, t, expected):
    assert load("t09_is_subsequence").is_subsequence(s, t) is expected


# ---------- t10 ★ ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([3, 1, 4, 4, 2], 3),
        ([5, 5], None),
        ([-1, -2], -2),
        ([], None),
        ([1, 2, 3], 2),
        ([3, 3, 2], 2),
    ],
)
def test_t10_second_largest(nums, expected):
    assert load("t10_second_largest").second_largest(nums) == expected


def test_t10_no_sort():
    source = inspect.getsource(load("t10_second_largest").second_largest)
    assert "sort" not in source, "сортировать нельзя по условию"

import importlib
import inspect
import os
import random
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


def body(func):
    """Исходник функции без docstring — для проверок «не используй ...»."""
    source = inspect.getsource(func)
    doc = func.__doc__
    return source.replace(doc, "") if doc else source


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (".,", True),
        ("0P", False),
        ("", True),
        ("Аа", True),
    ],
)
def test_t01_valid_palindrome(s, expected):
    assert load("t01_valid_palindrome").valid_palindrome(s) is expected


def test_t01_no_copy():
    source = body(load("t01_valid_palindrome").valid_palindrome)
    assert "[::-1]" not in source and "reversed(" not in source and "join(" not in source


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([1, 3, 4, 6, 9], 7, [0, 3]),
        ([1, 2], 10, []),
        ([], 1, []),
        ([-3, -1, 0, 4], -4, [0, 1]),
    ],
)
def test_t02_two_sum_sorted(nums, target, expected):
    assert load("t02_two_sum_sorted").two_sum_sorted(nums, target) == expected


def test_t02_linear():
    nums = list(range(200_000))
    result, spent = timed(load("t02_two_sum_sorted").two_sum_sorted, nums, 399_997)
    assert result == [199_998, 199_999]
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),
        ([1, 2, -2, -1], []),
        ([], []),
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
    ],
)
def test_t03_three_sum(nums, expected):
    assert load("t03_three_sum").three_sum(nums) == expected


def test_t03_quadratic_enough():
    nums = list(range(-750, 750))
    random.Random(3).shuffle(nums)
    result, spent = timed(load("t03_three_sum").three_sum, nums)
    assert len(result) == len({tuple(t) for t in result})
    assert spent < 2, f"{spent:.2f} с — похоже на O(n³)"


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("heights", "expected"),
    [([1, 8, 6, 2, 5, 4, 8, 3, 7], 49), ([1, 1], 1), ([4], 0), ([], 0), ([4, 3, 2, 1, 4], 16)],
)
def test_t04_max_area(heights, expected):
    assert load("t04_max_area").max_area(heights) == expected


def test_t04_linear():
    heights = list(range(100_000))
    result, spent = timed(load("t04_max_area").max_area, heights)
    assert result == 2_499_950_000
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t05 ----------
@pytest.mark.parametrize(
    ("nums", "k", "prefix"),
    [([1, 1, 2, 2, 3], 3, [1, 2, 3]), ([], 0, []), ([5], 1, [5]), ([0, 0, 0], 1, [0]), ([1, 2, 3], 3, [1, 2, 3])],
)
def test_t05_remove_duplicates(nums, k, prefix):
    before = id(nums)
    assert load("t05_remove_duplicates").remove_duplicates(nums) == k
    assert nums[:k] == prefix and id(nums) == before


# ---------- t06 ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([-4, -1, 0, 3, 10], [0, 1, 9, 16, 100]),
        ([-7, -3, 2, 3, 11], [4, 9, 9, 49, 121]),
        ([], []),
        ([-3, -2, -1], [1, 4, 9]),
    ],
)
def test_t06_sorted_squares(nums, expected):
    assert load("t06_sorted_squares").sorted_squares(nums) == expected


def test_t06_no_sort():
    assert not re.search(r"\bsorted\(|\.sort\(", body(load("t06_sorted_squares").sorted_squares))


# ---------- t07 ★ ----------
@pytest.mark.parametrize(
    ("a", "m", "b", "expected"),
    [
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], [1, 2, 2, 3, 5, 6]),
        ([0], 0, [1], [1]),
        ([1], 1, [], [1]),
        ([4, 5, 0, 0], 2, [1, 2], [1, 2, 4, 5]),
    ],
)
def test_t07_merge_in_place(a, m, b, expected):
    assert load("t07_merge_in_place").merge_in_place(a, m, b, len(b)) is None
    assert a == expected


# ---------- t08 ★ ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [("aba", True), ("abca", True), ("abc", False), ("", True), ("deeee", True), ("eccer", True), ("abcdef", False), ("abccdba", True)],
)
def test_t08_almost_palindrome(s, expected):
    assert load("t08_almost_palindrome").almost_palindrome(s) is expected


# ---------- t09 ★ ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [("hello", "holle"), ("leetcode", "leotcede"), ("xyz", "xyz"), ("aA", "Aa"), ("", "")],
)
def test_t09_reverse_vowels(s, expected):
    assert load("t09_reverse_vowels").reverse_vowels(s) == expected


# ---------- t10 ★ ----------
@pytest.mark.parametrize(
    ("heights", "expected"),
    [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6), ([4, 2, 0, 3, 2, 5], 9), ([], 0), ([3, 0, 3], 3)],
)
def test_t10_trap_water(heights, expected):
    assert load("t10_trap_water").trap_water(heights) == expected

import importlib
import inspect
import os
import re
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")
BIG = list(range(0, 2_000_000, 2))  # 1 000 000 отсортированных чётных чисел


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


def no_shortcuts(func):
    source = inspect.getsource(func)
    assert "bisect" not in source and ".index(" not in source, "бинпоиск нужно написать самому"
    assert not re.search(r"\bin nums\b", source), "проверка `in` по списку — это O(n)"


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [([-1, 0, 3, 5, 9, 12], 9, 4), ([-1, 0, 3, 5, 9, 12], 2, -1), ([], 1, -1), ([5], 5, 0), ([1, 2], 2, 1)],
)
def test_t01_binary_search(nums, target, expected):
    assert load("t01_binary_search").binary_search(nums, target) == expected


def test_t01_log_time():
    func = load("t01_binary_search").binary_search
    no_shortcuts(func)
    start = time.perf_counter()
    for t in range(0, 200_000, 2):
        assert func(BIG, t) == t // 2
    assert time.perf_counter() - start < 1.5, "похоже на O(n)"


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [([1, 3, 5, 6], 5, 2), ([1, 3, 5, 6], 2, 1), ([1, 3, 5, 6], 7, 4), ([], 3, 0), ([1, 3, 5, 6], 0, 0)],
)
def test_t02_search_insert(nums, target, expected):
    assert load("t02_search_insert").search_insert(nums, target) == expected


def test_t02_log_time():
    func = load("t02_search_insert").search_insert
    no_shortcuts(func)
    start = time.perf_counter()
    for t in range(1, 200_001, 2):
        func(BIG, t)
    assert time.perf_counter() - start < 1.5, "похоже на O(n)"


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [([5, 7, 7, 8, 8, 10], 8, [3, 4]), ([5, 7, 7, 8, 8, 10], 6, [-1, -1]), ([], 0, [-1, -1]), ([1], 1, [0, 0]), ([2, 2], 3, [-1, -1])],
)
def test_t03_search_range(nums, target, expected):
    assert load("t03_search_range").search_range(nums, target) == expected


def test_t03_log_time_on_equal_values():
    func = load("t03_search_range").search_range
    no_shortcuts(func)
    nums = [7] * 1_000_000
    start = time.perf_counter()
    for _ in range(1000):
        assert func(nums, 7) == [0, 999_999]
    assert time.perf_counter() - start < 1.0, "похоже на проход влево-вправо, O(n)"


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [([4, 5, 6, 7, 0, 1, 2], 0, 4), ([4, 5, 6, 7, 0, 1, 2], 3, -1), ([1], 1, 0), ([1], 0, -1), ([3, 1], 1, 1), ([5, 1, 3], 5, 0)],
)
def test_t04_search_rotated(nums, target, expected):
    assert load("t04_search_rotated").search_rotated(nums, target) == expected


def test_t04_log_time():
    func = load("t04_search_rotated").search_rotated
    no_shortcuts(func)
    nums = BIG[500_000:] + BIG[:500_000]
    start = time.perf_counter()
    for t in range(0, 100_000, 2):
        assert func(nums, t) == 500_000 + t // 2
    assert time.perf_counter() - start < 1.5, "похоже на O(n)"


# ---------- t05 ----------
@pytest.mark.parametrize(("x", "expected"), [(8, 2), (16, 4), (0, 0), (1, 1), (2, 1), (10**18, 10**9), (10**18 - 1, 10**9 - 1)])
def test_t05_int_sqrt(x, expected):
    assert load("t05_int_sqrt").int_sqrt(x) == expected


def test_t05_no_math():
    source = inspect.getsource(load("t05_int_sqrt").int_sqrt)
    assert "sqrt(" not in source.replace("def int_sqrt(", "") and "** 0.5" not in source and "**0.5" not in source


# ---------- t06 ----------
@pytest.mark.parametrize(
    ("piles", "h", "expected"),
    [([3, 6, 7, 11], 8, 4), ([30, 11, 23, 4, 20], 5, 30), ([30, 11, 23, 4, 20], 6, 23), ([1], 1, 1), ([1_000_000_000], 2, 500_000_000)],
)
def test_t06_min_eating_speed(piles, h, expected):
    assert load("t06_min_eating_speed").min_eating_speed(piles, h) == expected


# ---------- t07 ★ ----------
@pytest.mark.parametrize(("nums", "expected"), [([3, 4, 5, 1, 2], 1), ([4, 5, 6, 7, 0, 1, 2], 0), ([11, 13, 15], 11), ([2, 1], 1), ([5], 5)])
def test_t07_find_min_rotated(nums, expected):
    assert load("t07_find_min_rotated").find_min_rotated(nums) == expected


# ---------- t08 ★ ----------
@pytest.mark.parametrize("nums", [[1, 2, 3, 1], [1, 2, 1, 3, 5, 6, 4], [1], [2, 1], [1, 2]])
def test_t08_peak_element(nums):
    i = load("t08_peak_element").peak_element(nums)
    left = nums[i - 1] if i > 0 else float("-inf")
    right = nums[i + 1] if i < len(nums) - 1 else float("-inf")
    assert left < nums[i] > right


# ---------- t09 ★ ----------
MATRIX = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]


@pytest.mark.parametrize(("matrix", "target", "expected"), [(MATRIX, 3, True), (MATRIX, 13, False), ([], 1, False), (MATRIX, 60, True), ([[1]], 2, False)])
def test_t09_search_matrix(matrix, target, expected):
    assert load("t09_search_matrix").search_matrix(matrix, target) is expected


# ---------- t10 ★ ----------
@pytest.mark.parametrize(
    ("weights", "days", "expected"),
    [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 15), ([3, 2, 2, 4, 1, 4], 3, 6), ([1, 2, 3, 1, 1], 4, 3), ([5], 1, 5)],
)
def test_t10_ship_capacity(weights, days, expected):
    assert load("t10_ship_capacity").ship_capacity(weights, days) == expected

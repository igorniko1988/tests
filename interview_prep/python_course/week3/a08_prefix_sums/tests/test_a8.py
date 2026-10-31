import importlib
import inspect
import os
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 ----------
def test_t01_range_sum():
    nums = [-2, 0, 3, -5, 2, -1]
    rs = load("t01_range_sum").RangeSum(nums)
    assert (rs.query(0, 2), rs.query(2, 5), rs.query(0, 5), rs.query(3, 3)) == (1, -1, -3, -5)
    nums[0] = 100
    assert rs.query(0, 2) == 1
    for bad in [(3, 2), (-1, 2), (0, 6)]:
        with pytest.raises(IndexError):
            rs.query(*bad)


def test_t01_constant_queries():
    rs = load("t01_range_sum").RangeSum(list(range(100_000)))
    start = time.perf_counter()
    for i in range(200_000):
        rs.query(0, 99_999)
    assert time.perf_counter() - start < 1.0, "запрос должен быть O(1)"


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [([1, 1, 1], 2, 2), ([1, 2, 3], 3, 2), ([1, -1, 0], 0, 3), ([], 0, 0), ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4)],
)
def test_t02_subarray_sum_k(nums, k, expected):
    assert load("t02_subarray_sum_k").subarray_sum_k(nums, k) == expected


def test_t02_linear():
    start = time.perf_counter()
    assert load("t02_subarray_sum_k").subarray_sum_k([0] * 100_000, 0) == 100_000 * 100_001 // 2
    assert time.perf_counter() - start < 1.0, "похоже на O(n²)"


# ---------- t03 ----------
@pytest.mark.parametrize(("nums", "expected"), [([1, 7, 3, 6, 5, 6], 3), ([1, 2, 3], -1), ([2, 1, -1], 0), ([], -1), ([0], 0)])
def test_t03_pivot_index(nums, expected):
    assert load("t03_pivot_index").pivot_index(nums) == expected


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [([0, 1], 2), ([0, 1, 0], 2), ([0, 0, 1, 0, 0, 0, 1, 1], 6), ([1, 1], 0), ([], 0), ([1, 0, 1, 1, 0, 0], 6)],
)
def test_t04_contiguous_array(nums, expected):
    assert load("t04_contiguous_array").contiguous_array(nums) == expected


def test_t04_linear():
    start = time.perf_counter()
    assert load("t04_contiguous_array").contiguous_array([0, 1] * 50_000) == 100_000
    assert time.perf_counter() - start < 1.0


# ---------- t05 ----------
@pytest.mark.parametrize(("nums", "expected"), [([1, 2, 3, 4], [1, 3, 6, 10]), ([3, -1], [3, 2]), ([], [])])
def test_t05_running_sum(nums, expected):
    before = list(nums)
    assert load("t05_running_sum").running_sum(nums) == expected
    assert nums == before


def test_t05_no_accumulate():
    assert "accumulate" not in inspect.getsource(load("t05_running_sum").running_sum)


# ---------- t06 ----------
@pytest.mark.parametrize(("nums", "expected"), [([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6), ([-3, -1, -2], -1), ([5], 5), ([5, 4, -1, 7, 8], 23)])
def test_t06_max_subarray(nums, expected):
    assert load("t06_max_subarray").max_subarray(nums) == expected


def test_t06_linear():
    start = time.perf_counter()
    assert load("t06_max_subarray").max_subarray([1, -1] * 100_000) == 1
    assert time.perf_counter() - start < 1.0, "похоже на O(n²)"


# ---------- t07 ★ ----------
def test_t07_range_sum_2d():
    m = load("t07_range_sum_2d").RangeSum2D([[3, 0, 1], [5, 6, 3], [1, 2, 0]])
    assert m.query(1, 1, 2, 2) == 11
    assert m.query(0, 0, 0, 0) == 3
    assert m.query(0, 0, 2, 2) == 21
    assert m.query(0, 1, 1, 2) == 10


# ---------- t08 ★ ----------
@pytest.mark.parametrize(("nums", "k", "expected"), [([4, 5, 0, -2, -3, 1], 5, 7), ([5], 9, 0), ([0, 0], 3, 3)])
def test_t08_divisible_by_k(nums, k, expected):
    assert load("t08_divisible_by_k").divisible_by_k(nums, k) == expected


# ---------- t09 ★ ----------
def test_t09_range_updates():
    func = load("t09_range_updates").range_updates
    assert func(5, [(1, 3, 2), (2, 4, 3), (0, 2, -2)]) == [-2, 0, 3, 5, 3]
    assert func(3, []) == [0, 0, 0]
    start = time.perf_counter()
    result = func(100_000, [(0, 99_999, 1)] * 100_000)
    assert result[0] == 100_000 and result[-1] == 100_000
    assert time.perf_counter() - start < 1.0, "похоже на O(n · updates)"


# ---------- t10 ★ ----------
@pytest.mark.parametrize(("nums", "k", "expected"), [([1, -1, 5, -2, 3], 3, 4), ([-2, -1, 2, 1], 1, 2), ([1, 2], 7, 0), ([3], 3, 1)])
def test_t10_longest_sum_k(nums, k, expected):
    assert load("t10_longest_sum_k").longest_sum_k(nums, k) == expected

import importlib
import os
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в папках частей.
SRC = os.environ.get("SRC", "tasks")
SECTION = {
    "t01_pair_difference": "p3_algo",
    "t02_decode": "p3_algo",
    "t03_compare_responses": "p4_aqa",
}
TIME_LIMIT = 0.5  # секунды; O(n²) на этих размерах не укладывается


def load(name):
    package = SECTION[name] if SRC == "tasks" else SRC
    return importlib.import_module(f"{package}.{name}")


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([5, 20, 3, 2, 50, 80], 78, True),
        ([90, 70, 20, 80, 50], 45, False),
        ([1, 2, 1], 0, True),
        ([1, 2, 3], 0, False),
        ([], 1, False),
        ([7], 0, False),
        ([3, 1], 2, True),
        ([-1, -5], 4, True),
    ],
)
def test_t01_pair_difference(nums, k, expected):
    assert load("t01_pair_difference").pair_difference(nums, k) is expected


def test_t01_linear():
    nums = list(range(0, 200_000, 2))
    result, spent = timed(load("t01_pair_difference").pair_difference, nums, 1)
    assert result is False
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("a3b1", "aaab"),
        ("a2b1c5a2", "aabcccccaa"),
        ("z12", "z" * 12),
        ("", ""),
        ("a1", "a"),
        ("x10y2", "x" * 10 + "yy"),
    ],
)
def test_t02_decode(s, expected):
    assert load("t02_decode").decode(s) == expected


# ---------- t03 ----------
def test_t03_example():
    expected = [{"id": 1, "s": "NEW"}, {"id": 2, "s": "NEW"}, {"id": 3, "s": "NEW"}]
    actual = [{"id": 2, "s": "FILLED"}, {"id": 3, "s": "NEW"}, {"id": 4, "s": "NEW"}, {"id": 3, "s": "NEW"}]
    assert load("t03_compare_responses").compare_responses(expected, actual) == {
        "missing": [1],
        "extra": [4],
        "mismatched": [2],
        "duplicated": [3],
    }


def test_t03_equal_lists_in_other_order():
    expected = [{"id": 2, "a": 1}, {"id": 1, "a": 2}]
    actual = [{"id": 1, "a": 2}, {"id": 2, "a": 1}]
    assert load("t03_compare_responses").compare_responses(expected, actual) == {
        "missing": [],
        "extra": [],
        "mismatched": [],
        "duplicated": [],
    }


def test_t03_sorted_and_first_record_wins():
    expected = [{"id": 9, "a": 1}, {"id": 5, "a": 1}, {"id": 7, "a": 1}]
    actual = [{"id": 8}, {"id": 6}, {"id": 7, "a": 1}, {"id": 7, "a": 2}, {"id": 6}]
    assert load("t03_compare_responses").compare_responses(expected, actual) == {
        "missing": [5, 9],
        "extra": [6, 8],
        "mismatched": [],
        "duplicated": [6, 7],
    }


def test_t03_empty():
    assert load("t03_compare_responses").compare_responses([], []) == {
        "missing": [],
        "extra": [],
        "mismatched": [],
        "duplicated": [],
    }


def test_t03_linear():
    expected = [{"id": i, "a": 1} for i in range(20_000)]
    actual = list(reversed(expected))
    result, spent = timed(load("t03_compare_responses").compare_responses, expected, actual)
    assert result == {"missing": [], "extra": [], "mismatched": [], "duplicated": []}
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n·m)"

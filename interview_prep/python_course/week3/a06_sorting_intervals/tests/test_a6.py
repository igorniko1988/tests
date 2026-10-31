import copy
import importlib
import inspect
import os
import random
import re
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("intervals", "expected"),
    [
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([[1, 10], [2, 3]], [[1, 10]]),
        ([], []),
        ([[5, 6], [1, 2]], [[1, 2], [5, 6]]),
    ],
)
def test_t01_merge_intervals(intervals, expected):
    before = copy.deepcopy(intervals)
    assert load("t01_merge_intervals").merge_intervals(intervals) == expected
    assert intervals == before, "вход не должен меняться"


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("intervals", "new", "expected"),
    [
        ([[1, 3], [6, 9]], [2, 5], [[1, 5], [6, 9]]),
        ([[1, 2], [3, 5], [6, 7], [8, 10]], [4, 8], [[1, 2], [3, 10]]),
        ([], [5, 7], [[5, 7]]),
        ([[1, 5]], [6, 8], [[1, 5], [6, 8]]),
        ([[3, 5]], [1, 2], [[1, 2], [3, 5]]),
        ([[1, 5]], [5, 7], [[1, 7]]),
    ],
)
def test_t02_insert_interval(intervals, new, expected):
    assert load("t02_insert_interval").insert_interval(intervals, new) == expected


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("meetings", "expected"),
    [([[0, 30], [5, 10], [15, 20]], 2), ([[7, 10], [2, 4]], 1), ([[1, 5], [5, 10]], 1), ([], 0), ([[1, 4], [2, 5], [3, 6]], 3)],
)
def test_t03_min_rooms(meetings, expected):
    assert load("t03_min_rooms").min_rooms(meetings) == expected


def test_t03_fast():
    rnd = random.Random(5)
    meetings = []
    for _ in range(100_000):
        s = rnd.randrange(1_000_000)
        meetings.append([s, s + rnd.randrange(1, 100)])
    start = time.perf_counter()
    load("t03_min_rooms").min_rooms(meetings)
    assert time.perf_counter() - start < 1.5, "похоже на O(n²)"


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]), ([2, 0, 1], [0, 1, 2]), ([], []), ([1], [1]), ([2, 2, 0, 0], [0, 0, 2, 2])],
)
def test_t04_sort_colors(nums, expected):
    before = id(nums)
    assert load("t04_sort_colors").sort_colors(nums) is None
    assert nums == expected and id(nums) == before


def test_t04_no_sort_and_no_count():
    source = inspect.getsource(load("t04_sort_colors").sort_colors)
    assert not re.search(r"\bsorted\(|\.sort\(|\.count\(", source)


# ---------- t05 ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [([10, 2], "210"), ([3, 30, 34, 5, 9], "9534330"), ([0, 0], "0"), ([1], "1"), ([432, 43243], "43243432")],
)
def test_t05_largest_number(nums, expected):
    assert load("t05_largest_number").largest_number(nums) == expected


# ---------- t06 ----------
@pytest.mark.parametrize(
    ("intervals", "expected"),
    [([[1, 2], [2, 3], [3, 4], [1, 3]], 1), ([[1, 2], [1, 2], [1, 2]], 2), ([[1, 2], [2, 3]], 0), ([], 0), ([[1, 100], [11, 22], [1, 11], [2, 12]], 2)],
)
def test_t06_erase_overlap(intervals, expected):
    assert load("t06_erase_overlap").erase_overlap(intervals) == expected


# ---------- t07 ★ ----------
@pytest.mark.parametrize(
    ("meetings", "expected"),
    [([[0, 30], [5, 10], [15, 20]], False), ([[7, 10], [2, 4]], True), ([[1, 5], [5, 6]], True), ([], True)],
)
def test_t07_can_attend(meetings, expected):
    assert load("t07_can_attend").can_attend(meetings) is expected


# ---------- t08 ★ ----------
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [([[0, 2], [5, 10]], [[1, 5], [8, 12]], [[1, 2], [5, 5], [8, 10]]), ([], [[1, 2]], []), ([[1, 7]], [[3, 4]], [[3, 4]])],
)
def test_t08_interval_intersection(a, b, expected):
    assert load("t08_interval_intersection").interval_intersection(a, b) == expected


# ---------- t09 ★ ----------
@pytest.mark.parametrize("nums", [[5, 2, 4, 6, 1, 3], [], [1], [3, 3, 1], list(range(50, 0, -1))])
def test_t09_merge_sort(nums, expected=None):
    result = load("t09_merge_sort").merge_sort(nums)
    assert result == sorted(nums) and result is not nums


def test_t09_stable_and_no_builtin():
    module = load("t09_merge_sort")

    class Item:
        def __init__(self, key, tag):
            self.key, self.tag = key, tag

        def __le__(self, other):
            return self.key <= other.key

        def __lt__(self, other):
            return self.key < other.key

    items = [Item(1, "a"), Item(0, "x"), Item(1, "b")]
    assert [i.tag for i in module.merge_sort(items)] == ["x", "a", "b"]
    assert not re.search(r"\bsorted\(|\.sort\(|heapq", inspect.getsource(module.merge_sort))


# ---------- t10 ★ ----------
@pytest.mark.parametrize(
    ("points", "k", "expected"),
    [([[1, 3], [-2, 2]], 1, [[-2, 2]]), ([[3, 3], [5, -1], [-2, 4]], 2, [[3, 3], [-2, 4]]), ([[1, 0], [0, 1]], 2, [[1, 0], [0, 1]])],
)
def test_t10_k_closest(points, k, expected):
    assert load("t10_k_closest").k_closest(points, k) == expected

import importlib
import importlib.util
import os
import sys
import random
import time
from pathlib import Path

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в папках разделов.
SRC = os.environ.get("SRC", "tasks")
SECTION = {
    "t02_has_duplicate": "s07_method",
    "t03_count_pairs": "s07_method",
    "t04_common_ids": "s07_method",
}
TIME_LIMIT = 0.2  # секунды: O(n) укладывается с запасом, O(n²) — нет


# Обязательные задачи вынесены в todo/<модуль>; если файл там — берём его.
TODO = Path(__file__).resolve().parents[2] / "todo" / "a0"


def load_file(path):
    name = f"todo_{path.parent.name}_{path.stem}"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def load(name):
    if SRC == "tasks" and (TODO / f"{name}.py").exists():
        return load_file(TODO / f"{name}.py")
    package = SECTION[name] if SRC == "tasks" else SRC
    return importlib.import_module(f"{package}.{name}")


def timed(func, *args):
    start = time.perf_counter()
    result = func(*args)
    return result, time.perf_counter() - start


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([1, 2, 3, 1], True),
        ([1, 2, 3], False),
        ([], False),
        ([7], False),
        (["a", "A"], False),
        ([5, 5], True),
    ],
)
def test_t02_correct(items, expected):
    assert load("t02_has_duplicate").has_duplicate(items) is expected


def test_t02_does_not_change_input():
    items = [3, 1, 3]
    load("t02_has_duplicate").has_duplicate(items)
    assert items == [3, 1, 3]


def test_t02_fast():
    items = list(range(10_000))  # повторов нет — худший случай, надо пройти всё
    result, seconds = timed(load("t02_has_duplicate").has_duplicate, items)
    assert result is False
    assert seconds < TIME_LIMIT, f"{seconds:.2f} с — похоже на O(n²)"


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([1, 2, 3, 4], 5, 2),
        ([3, 3, 3], 6, 3),
        ([1, 1], 3, 0),
        ([], 0, 0),
        ([-1, 1, 0, 0], 0, 2),
        ([5], 10, 0),
        ([2, 2, 2, 2], 4, 6),
    ],
)
def test_t03_correct(nums, target, expected):
    assert load("t03_count_pairs").count_pairs(nums, target) == expected


def test_t03_matches_brute_force_on_random():
    rng = random.Random(1)
    for _ in range(50):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 30))]
        target = rng.randint(-6, 6)
        expected = sum(
            1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] + nums[j] == target
        )
        assert load("t03_count_pairs").count_pairs(nums, target) == expected, (nums, target)


def test_t03_fast():
    nums = list(range(10_000))
    result, seconds = timed(load("t03_count_pairs").count_pairs, nums, 9_999)
    assert result == 5_000
    assert seconds < TIME_LIMIT, f"{seconds:.2f} с — похоже на O(n²)"


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([3, 1, 2], [2, 3], [3, 2]),
        ([1, 1, 2], [1], [1]),
        ([1, 2], [3, 4], []),
        ([], [1], []),
        ([1, 2], [], []),
        (["x", "y", "x"], ["x", "y", "y"], ["x", "y"]),
    ],
)
def test_t04_correct(a, b, expected):
    assert load("t04_common_ids").common_ids(a, b) == expected


def test_t04_does_not_change_input():
    a, b = [2, 1, 2], [2]
    load("t04_common_ids").common_ids(a, b)
    assert (a, b) == ([2, 1, 2], [2])


def test_t04_fast():
    a = list(range(10_000))
    b = list(range(5_000, 15_000))
    result, seconds = timed(load("t04_common_ids").common_ids, a, b)
    assert result == list(range(5_000, 10_000))
    assert seconds < TIME_LIMIT, f"{seconds:.2f} с — похоже на O(n · m)"

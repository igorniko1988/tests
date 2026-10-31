import importlib
import os
import random
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в папках частей.
SRC = os.environ.get("SRC", "tasks")
SECTION = {
    "t01_lru_cache": "p3_lru",
    "t02_first_bad_build": "p4_algo",
    "t03_peak_sessions": "p4_algo",
}


def load(name):
    package = SECTION[name] if SRC == "tasks" else SRC
    return importlib.import_module(f"{package}.{name}")


# ---------- t01 ----------
def test_t01_lru():
    LRUCache = load("t01_lru_cache").LRUCache
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)
    assert c.keys() == ["a", "c"] and c.get("b") is None and len(c) == 2
    c.put("a", 10)
    c.put("d", 4)
    assert c.keys() == ["a", "d"] and c.get("a") == 10
    with pytest.raises(ValueError):
        LRUCache(0)


def test_t01_lru_fast():
    c = load("t01_lru_cache").LRUCache(1000)
    start = time.perf_counter()
    for i in range(100_000):
        c.put(i, i)
        c.get(i - 10)
    assert time.perf_counter() - start < 1.5, "get/put должны быть O(1)"


# ---------- t02 ----------
@pytest.mark.parametrize(("n", "bad_from", "expected"), [(5, 4, 4), (1, 1, 1), (3, None, -1), (10, 1, 1), (10, 10, 10)])
def test_t02_first_bad_build(n, bad_from, expected):
    def is_bad(build):
        return bad_from is not None and build >= bad_from

    assert load("t02_first_bad_build").first_bad_build(n, is_bad) == expected


def test_t02_log_calls():
    calls = []

    def is_bad(build):
        calls.append(build)
        return build >= 777_777

    assert load("t02_first_bad_build").first_bad_build(1_000_000, is_bad) == 777_777
    assert len(calls) <= 21, f"{len(calls)} прогонов — нужно O(log n)"


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("sessions", "expected"),
    [
        ([[1, 5], [2, 6], [5, 7]], (2, 2)),
        ([[1, 3], [3, 5]], (1, 1)),
        ([[0, 10], [1, 2], [1, 3]], (3, 1)),
        ([], (0, None)),
        ([[5, 6]], (1, 5)),
    ],
)
def test_t03_peak_sessions(sessions, expected):
    assert load("t03_peak_sessions").peak_sessions(sessions) == expected


def test_t03_fast():
    rnd = random.Random(7)
    sessions = []
    for _ in range(100_000):
        s = rnd.randrange(1_000_000)
        sessions.append([s, s + rnd.randrange(1, 50)])
    start = time.perf_counter()
    peak, _ = load("t03_peak_sessions").peak_sessions(sessions)
    assert peak >= 1
    assert time.perf_counter() - start < 1.5, "похоже на O(n²)"

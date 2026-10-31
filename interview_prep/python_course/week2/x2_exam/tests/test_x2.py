import importlib
import os
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в папках частей.
SRC = os.environ.get("SRC", "tasks")
SECTION = {
    "t01_retry": "p3_retry",
    "t02_backspace_compare": "p4_algo",
    "t03_longest_ones": "p4_algo",
}


def load(name):
    package = SECTION[name] if SRC == "tasks" else SRC
    return importlib.import_module(f"{package}.{name}")


def flaky(failures, error=ConnectionError):
    calls = []

    def func(*args, **kwargs):
        calls.append(args)
        if len(calls) <= failures:
            raise error("boom")
        return 100

    return func, calls


# ---------- t01 ----------
def test_t01_retry_succeeds():
    func, calls = flaky(2)
    wrapped = load("t01_retry").retry(times=3, exceptions=(ConnectionError,))(func)
    assert wrapped(7) == 100 and calls == [(7,), (7,), (7,)]


def test_t01_retry_gives_up_and_sleeps(monkeypatch):
    module = load("t01_retry")
    sleeps = []
    monkeypatch.setattr(module.time, "sleep", sleeps.append)
    func, calls = flaky(9)
    with pytest.raises(ConnectionError):
        module.retry(times=3, exceptions=(ConnectionError,), delay=0.2)(func)()
    assert len(calls) == 3 and sleeps == [0.2, 0.2]


def test_t01_retry_other_errors_and_validation():
    retry = load("t01_retry").retry
    func, calls = flaky(9, error=KeyError)
    with pytest.raises(KeyError):
        retry(exceptions=(ConnectionError,))(func)()
    assert len(calls) == 1
    with pytest.raises(ValueError):
        retry(times=0)


def test_t01_retry_wraps():
    @load("t01_retry").retry()
    def get_price():
        """Price."""
        return 1

    assert get_price.__name__ == "get_price" and get_price.__doc__ == "Price."


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [("ab#c", "ad#c", True), ("ab##", "c#d#", True), ("a#c", "b", False), ("#a", "a", True), ("", "#", True), ("a##b", "b", True)],
)
def test_t02_backspace_compare(s, t, expected):
    assert load("t02_backspace_compare").backspace_compare(s, t) is expected


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2, 6),
        ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3, 10),
        ([0, 0], 0, 0),
        ([], 1, 0),
        ([0, 0, 0], 5, 3),
    ],
)
def test_t03_longest_ones(nums, k, expected):
    assert load("t03_longest_ones").longest_ones(nums, k) == expected


def test_t03_linear():
    nums = [1, 0] * 100_000
    start = time.perf_counter()
    assert load("t03_longest_ones").longest_ones(nums, 1000) == 2001
    assert time.perf_counter() - start < 1.0, "похоже на O(n²)"

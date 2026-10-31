import importlib
import os
import re
from itertools import count, islice

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


def flaky(failures, error=ConnectionError, result=100):
    calls = []

    def func():
        calls.append(1)
        if len(calls) <= failures:
            raise error("boom")
        return result

    return func, calls


# ---------- t01 ----------
def test_t01_backoff_and_attempts():
    pauses = []
    func, calls = flaky(3)
    wrapped = load("t01_retry").retry(times=4, delay=0.5, backoff=2, sleep=pauses.append)(func)
    assert wrapped() == 100
    assert pauses == [0.5, 1.0, 2.0]
    assert wrapped.attempts == 4 and len(calls) == 4


def test_t01_gives_up_without_last_sleep():
    pauses = []
    func, calls = flaky(10, error=TimeoutError)
    wrapped = load("t01_retry").retry(times=3, delay=1, backoff=3, sleep=pauses.append)(func)
    with pytest.raises(TimeoutError):
        wrapped()
    assert pauses == [1, 3] and len(calls) == 3


def test_t01_other_errors_immediately():
    pauses = []
    func, calls = flaky(10, error=ValueError)
    wrapped = load("t01_retry").retry(sleep=pauses.append)(func)
    with pytest.raises(ValueError):
        wrapped()
    assert pauses == [] and len(calls) == 1


def test_t01_attempts_reset_and_wraps():
    pauses = []
    retry = load("t01_retry").retry

    @retry(times=2, sleep=pauses.append)
    def ok():
        """Doc."""
        return 1

    assert ok() == 1 and ok.attempts == 1
    assert ok.__name__ == "ok" and ok.__doc__ == "Doc."
    with pytest.raises(ValueError):
        retry(times=0)


# ---------- t02 ----------
def test_t02_passed_with_placeholders():
    log = []

    @load("t02_step").step("create order {symbol}", log)
    def create_order(*, symbol, qty):
        return {"symbol": symbol, "qty": qty}

    assert create_order(symbol="BTC", qty=1) == {"symbol": "BTC", "qty": 1}
    assert len(log) == 1
    assert re.fullmatch(r"STEP create order BTC: PASSED in \d+\.\d{2}s", log[0]), log[0]
    assert create_order.__name__ == "create_order"


def test_t02_failed_reraises():
    log = []

    @load("t02_step").step("login", log)
    def login(user):
        raise PermissionError(user)

    with pytest.raises(PermissionError):
        login("ann")
    assert log == ["STEP login: FAILED PermissionError"]


# ---------- t03 ★ ----------
LINES = ["t1 INFO r1 start", "t2 ERROR r1 db down", "t3 ERROR r2 x", "bad", "t5 ERRORS r1 no"]


@pytest.mark.parametrize(
    ("kwargs", "numbers"),
    [
        ({"level": "ERROR"}, [2, 3]),
        ({"level": "ERROR", "request_id": "r1"}, [2]),
        ({"request_id": "r1"}, [1, 2, 5]),
        ({}, [1, 2, 3, 5]),
    ],
)
def test_t03_filter_log(kwargs, numbers):
    result = list(load("t03_filter_log").filter_log(LINES, **kwargs))
    assert [n for n, _ in result] == numbers
    assert all(LINES[n - 1] == line for n, line in result)


def test_t03_lazy():
    stream = (f"t{i} ERROR r{i % 2} m" for i in count())
    result = load("t03_filter_log").filter_log(stream, request_id="r1")
    assert [n for n, _ in islice(result, 2)] == [2, 4]


# ---------- t04 ----------
def test_t04_example():
    def send(batch):
        if 3 in batch:
            raise ConnectionError

    assert load("t04_send_in_batches").send_in_batches(range(1, 8), 3, send) == {"sent": 4, "failed": [0]}


def test_t04_generator_input_and_batches():
    sent = []
    items = (i for i in range(5))
    result = load("t04_send_in_batches").send_in_batches(items, 2, sent.append)
    assert sent == [[0, 1], [2, 3], [4]]
    assert result == {"sent": 5, "failed": []}


def test_t04_all_fail_and_empty():
    module = load("t04_send_in_batches")

    def boom(batch):
        raise RuntimeError

    assert module.send_in_batches([1, 2, 3], 1, boom) == {"sent": 0, "failed": [0, 1, 2]}
    assert module.send_in_batches([], 3, boom) == {"sent": 0, "failed": []}
    with pytest.raises(ValueError):
        module.send_in_batches([1], 0, boom)


# ---------- t05 ★ ----------
@pytest.mark.parametrize(
    ("nested", "expected"),
    [
        ([1, [2, [3, (4, 5)]], 6], [1, 2, 3, 4, 5, 6]),
        (["ab", ["cd"]], ["ab", "cd"]),
        ([[], [[]]], []),
        ([], []),
    ],
)
def test_t05_flatten(nested, expected):
    assert load("t05_flatten").flatten(nested) == expected


# ---------- t06 ----------
class FakeTime:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def clock(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


def test_t06_returns_value_when_ready():
    t = FakeTime()
    statuses = iter([None, None, {"status": "FILLED"}])
    result = load("t06_wait_until").wait_until(lambda: next(statuses), timeout=1, interval=0.1, clock=t.clock, sleep=t.sleep)
    assert result == {"status": "FILLED"}
    assert t.sleeps == [0.1, 0.1]


def test_t06_timeout_message():
    t = FakeTime()
    with pytest.raises(TimeoutError) as error:
        load("t06_wait_until").wait_until(
            lambda: 0, timeout=1, interval=0.25, message="order filled", clock=t.clock, sleep=t.sleep
        )
    assert str(error.value) == "order filled not met in 1s, last value: 0"
    assert t.sleeps == [0.25, 0.25, 0.25, 0.25]


def test_t06_checks_at_least_once():
    t = FakeTime()
    calls = []

    def ready():
        calls.append(1)
        return "ok"

    assert load("t06_wait_until").wait_until(ready, timeout=0, clock=t.clock, sleep=t.sleep) == "ok"
    with pytest.raises(TimeoutError):
        load("t06_wait_until").wait_until(lambda: False, timeout=0, clock=t.clock, sleep=t.sleep)
    assert len(calls) == 1 and t.sleeps == []


def test_t06_condition_errors_propagate():
    t = FakeTime()

    def broken():
        raise KeyError("status")

    with pytest.raises(KeyError):
        load("t06_wait_until").wait_until(broken, clock=t.clock, sleep=t.sleep)

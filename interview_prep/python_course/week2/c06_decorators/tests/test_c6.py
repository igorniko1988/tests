import importlib
import os
import re
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 ----------
def test_t01_timer_prints_and_stores(capsys):
    timer = load("t01_timer").timer

    @timer
    def slow_add(a, b):
        """Adds slowly."""
        time.sleep(0.05)
        return a + b

    assert slow_add(1, b=2) == 3
    out = capsys.readouterr().out.strip()
    assert re.fullmatch(r"slow_add took \d+\.\d{3}s", out), out
    assert 0.04 < slow_add.last_duration < 0.5
    assert slow_add.__name__ == "slow_add" and slow_add.__doc__ == "Adds slowly."


def test_t01_timer_updates_last_duration(capsys):
    timer = load("t01_timer").timer

    @timer
    def wait(seconds):
        time.sleep(seconds)

    wait(0.05)
    first = wait.last_duration
    wait(0)
    assert wait.last_duration < first


# ---------- t02 ----------
def test_t02_log_calls():
    log = []
    log_calls = load("t02_log_calls").log_calls

    @log_calls(log)
    def divide(a, b=1):
        """Divides."""
        return a / b

    assert divide(6, b=3) == 2.0
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    assert log == ["divide(6, b=3) -> 2.0", "divide(1, 0) raised ZeroDivisionError"]
    assert divide.__name__ == "divide" and divide.__doc__ == "Divides."


def test_t02_strings_use_repr():
    log = []

    @load("t02_log_calls").log_calls(log)
    def greet(name, *, punct="!"):
        return f"hi {name}{punct}"

    greet("Ann", punct="?")
    assert log == ["greet('Ann', punct='?') -> 'hi Ann?'"]


# ---------- t03 ----------
def make_flaky(failures, error=ConnectionError, result=100):
    calls = []

    def func(*args, **kwargs):
        calls.append((args, kwargs))
        if len(calls) <= failures:
            raise error("boom")
        return result

    return func, calls


def test_t03_succeeds_after_failures():
    func, calls = make_flaky(2)
    wrapped = load("t03_retry").retry(times=3, exceptions=(ConnectionError,))(func)
    assert wrapped(1, x=2) == 100
    assert len(calls) == 3 and calls[0] == ((1,), {"x": 2})


def test_t03_reraises_last_exception():
    func, calls = make_flaky(5)
    wrapped = load("t03_retry").retry(times=3, exceptions=(ConnectionError,))(func)
    with pytest.raises(ConnectionError):
        wrapped()
    assert len(calls) == 3


def test_t03_other_exceptions_not_retried():
    func, calls = make_flaky(5, error=KeyError)
    wrapped = load("t03_retry").retry(times=3, exceptions=(ConnectionError,))(func)
    with pytest.raises(KeyError):
        wrapped()
    assert len(calls) == 1


def test_t03_sleeps_between_attempts_only(monkeypatch):
    module = load("t03_retry")
    sleeps = []
    monkeypatch.setattr(module.time, "sleep", sleeps.append)
    func, _ = make_flaky(5)
    with pytest.raises(ConnectionError):
        module.retry(times=3, exceptions=(ConnectionError,), delay=0.5)(func)()
    assert sleeps == [0.5, 0.5]


def test_t03_defaults_and_validation():
    retry = load("t03_retry").retry
    func, calls = make_flaky(2, error=ValueError)

    @retry()
    def wrapped():
        """Doc."""
        return func()

    assert wrapped() == 100 and len(calls) == 3
    assert wrapped.__name__ == "wrapped"
    with pytest.raises(ValueError):
        retry(times=0)


# ---------- t04 ----------
def test_t04_count_calls():
    CountCalls = load("t04_count_calls").CountCalls

    @CountCalls
    def add(a, b=0):
        """Adds."""
        return a + b

    assert add(1, b=2) == 3
    assert add(5) == 5
    assert add.count == 2
    add.reset()
    assert add.count == 0
    assert add.__name__ == "add" and add.__doc__ == "Adds."


def test_t04_exception_counts():
    @load("t04_count_calls").CountCalls
    def boom():
        raise RuntimeError

    with pytest.raises(RuntimeError):
        boom()
    assert boom.count == 1


# ---------- t05 ----------
def test_t05_ttl_cache():
    now = [0.0]
    calls = []

    @load("t05_ttl_cache").ttl_cache(seconds=10, clock=lambda: now[0])
    def get_rate(symbol, *, side="buy"):
        calls.append((symbol, side))
        return len(calls)

    assert get_rate("BTC") == 1
    now[0] = 9.9
    assert get_rate("BTC") == 1
    assert get_rate("ETH") == 2
    now[0] = 10
    assert get_rate("BTC") == 3
    assert get_rate("BTC", side="sell") == 4
    assert get_rate("BTC", side="sell") == 4
    assert get_rate.__name__ == "get_rate"


def test_t05_kwargs_order():
    now = [0]
    calls = []

    @load("t05_ttl_cache").ttl_cache(5, clock=lambda: now[0])
    def f(**kw):
        calls.append(kw)
        return 1

    f(a=1, b=2)
    f(b=2, a=1)
    assert len(calls) == 1


# ---------- t06 ★ ----------
def test_t06_works_on_methods():
    Counted = load("t06_counted_method").Counted

    class Api:
        @Counted
        def get(self, path):
            return f"GET {path} {type(self).__name__}"

    a, b = Api(), Api()
    assert a.get("/x") == "GET /x Api"
    assert b.get(path="/y") == "GET /y Api"
    assert Api.get.count == 2


def test_t06_works_on_functions():
    @load("t06_counted_method").Counted
    def double(x):
        """Doubles."""
        return x * 2

    assert double(4) == 8 and double.count == 1
    assert double.__name__ == "double"

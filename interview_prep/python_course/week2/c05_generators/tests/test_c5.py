import importlib
import inspect
import os
import types
from itertools import count, islice

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ((0, 5), [0, 1, 2, 3, 4]),
        ((1, 10, 3), [1, 4, 7]),
        ((5, 0, -2), [5, 3, 1]),
        ((3, 3), []),
        ((5, 1), []),
        ((0, 1, 0.25), [0, 0.25, 0.5, 0.75]),
    ],
)
def test_t01_my_range(args, expected):
    assert list(load("t01_my_range").my_range(*args)) == expected


def test_t01_is_lazy_iterator():
    result = load("t01_my_range").my_range(0, 10**12)
    assert next(result) == 0 and next(result) == 1


def test_t01_zero_step_fails_on_call():
    with pytest.raises(ValueError):
        load("t01_my_range").my_range(0, 5, 0)


def test_t01_no_builtin_range():
    source = inspect.getsource(load("t01_my_range").my_range)
    assert "range(" not in source.replace("my_range(", ""), "range() использовать нельзя"


# ---------- t02 ----------
def test_t02_error_lines(tmp_path):
    log = tmp_path / "app.log"
    log.write_text("10:00 INFO start\n10:01 ERROR db timeout\n10:02 ERROR auth failed\n", encoding="utf-8")
    result = load("t02_error_lines").error_lines(log)
    assert isinstance(result, types.GeneratorType)
    assert list(result) == [(2, "10:01 ERROR db timeout"), (3, "10:02 ERROR auth failed")]


def test_t02_no_errors_and_last_line_without_newline(tmp_path):
    log = tmp_path / "app.log"
    log.write_text("a INFO x\nb ERROR y", encoding="utf-8")
    assert list(load("t02_error_lines").error_lines(log)) == [(2, "b ERROR y")]
    log.write_text("a INFO x\n", encoding="utf-8")
    assert list(load("t02_error_lines").error_lines(log)) == []


def test_t02_reads_lazily():
    source = inspect.getsource(load("t02_error_lines").error_lines)
    assert ".read(" not in source and "readlines" not in source, "читай файл построчно"


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("items", "n", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ("abc", 3, [["a", "b", "c"]]),
        ([], 2, []),
        ([1, 2], 5, [[1, 2]]),
    ],
)
def test_t03_batched(items, n, expected):
    assert list(load("t03_batched").batched(items, n)) == expected


def test_t03_infinite_and_generator_input():
    batched = load("t03_batched").batched
    assert list(islice(batched(count(), 3), 2)) == [[0, 1, 2], [3, 4, 5]]
    assert list(batched((x for x in range(3)), 2)) == [[0, 1], [2]]


def test_t03_bad_n_fails_on_call():
    with pytest.raises(ValueError):
        load("t03_batched").batched([1], 0)


# ---------- t04 ----------
def test_t04_example_and_laziness():
    data = {1: ["a", "b"], 2: ["c"]}
    p = load("t04_paginator").Paginator(lambda page: data.get(page, []))
    assert iter(p) is p
    assert next(p) == "a"
    assert p.pages_fetched == 1
    assert list(p) == ["b", "c"]
    assert p.pages_fetched == 3


def test_t04_stops_at_first_empty_page():
    calls = []

    def fetch(page):
        calls.append(page)
        return {1: [1], 3: [3]}.get(page, [])

    assert list(load("t04_paginator").Paginator(fetch)) == [1]
    assert calls == [1, 2]


def test_t04_empty_api():
    p = load("t04_paginator").Paginator(lambda page: [])
    assert list(p) == []
    assert list(p) == []
    assert p.pages_fetched == 1


def test_t04_not_a_generator_function():
    cls = load("t04_paginator").Paginator
    assert not inspect.isgeneratorfunction(cls.__next__), "нужен класс с __next__, а не генератор"


# ---------- t05 ----------
def test_t05_example():
    lines = ["t1 INFO a ok", "t2 ERROR b db down", "bad", "t3 ERROR c x"]
    module = load("t05_error_events")
    events = list(module.error_events(lines))
    assert [e["service"] for e in events] == ["b", "c"]
    assert events[0] == {"ts": "t2", "level": "ERROR", "service": "b", "msg": "db down"}


def test_t05_parse_and_only():
    module = load("t05_error_events")
    parsed = list(module.parse(["t WARN svc slow down", "x y"]))
    assert parsed == [{"ts": "t", "level": "WARN", "service": "svc", "msg": "slow down"}]
    assert list(module.only(parsed, "WARN")) == parsed
    assert list(module.only(parsed, "ERROR")) == []


def test_t05_works_on_infinite_stream():
    module = load("t05_error_events")
    stream = (f"t{i} {'ERROR' if i % 3 == 0 else 'INFO'} s{i} m" for i in count())
    result = module.error_events(stream)
    assert not isinstance(result, list)
    assert [e["service"] for e in islice(result, 3)] == ["s0", "s3", "s6"]


# ---------- t06 ★ ----------
@pytest.mark.parametrize(
    ("items", "key", "expected"),
    [
        ("aabaa", None, [("a", ["a", "a"]), ("b", ["b"]), ("a", ["a", "a"])]),
        ([1, 3, 2, 4, 5], lambda x: x % 2, [(1, [1, 3]), (0, [2, 4]), (1, [5])]),
        ([], None, []),
        ([None, None, 0], None, [(None, [None, None]), (0, [0])]),
    ],
)
def test_t06_group_consecutive(items, key, expected):
    assert list(load("t06_group_consecutive").group_consecutive(items, key=key)) == expected


def test_t06_lazy_and_no_itertools():
    module = load("t06_group_consecutive")
    stream = (i // 2 for i in count())
    assert list(islice(module.group_consecutive(stream), 2)) == [(0, [0, 0]), (1, [1, 1])]
    assert "itertools" not in inspect.getsource(module.group_consecutive)

import importlib
import importlib.util
import inspect
import os
import sys
import time
from pathlib import Path

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в папках разделов.
SRC = os.environ.get("SRC", "tasks")
SECTION = {
    "t01_remove_all": "s01_list",
    "t02_hash_map": "s03_dict",
    "t03_common_users": "s04_set",
    "t04_top_words": "s05_counter_defaultdict",
    "t05_group_orders": "s05_counter_defaultdict",
    "t06_recent_events": "s06_deque",
    "t07_sort_records": "s07_sorting",
}
TIME_LIMIT = 0.5  # секунды; O(n²) на этих размерах не укладывается


# Обязательные задачи вынесены в todo/<модуль>; если файл там — берём его.
TODO = Path(__file__).resolve().parents[2] / "todo" / "c3"


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


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("items", "value", "removed", "rest"),
    [
        ([1, 2, 2, 3, 2], 2, 3, [1, 3]),
        ([2, 2], 2, 2, []),
        ([1, 2], 9, 0, [1, 2]),
        ([], 1, 0, []),
        ([1, 1.0, True, "1"], 1, 3, ["1"]),
    ],
)
def test_t01_remove_all(items, value, removed, rest):
    assert load("t01_remove_all").remove_all(items, value) == removed
    assert items == rest


def test_t01_same_object():
    data = [0, 1, 0]
    alias = data
    load("t01_remove_all").remove_all(data, 0)
    assert alias is data and alias == [1], "менять нужно переданный список, а не создавать новый"


def test_t01_linear():
    data = [1, 7] * 15_000
    removed, spent = timed(load("t01_remove_all").remove_all, data, 7)
    assert removed == 15_000 and data == [1] * 15_000
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t02 ----------
def test_t02_put_get_overwrite():
    m = load("t02_hash_map").HashMap()
    m.put("a", 1)
    m.put("a", 2)
    m.put("b", 3)
    assert m.get("a") == 2 and m.get("b") == 3
    assert len(m) == 2


def test_t02_get_default_and_contains():
    m = load("t02_hash_map").HashMap()
    m.put((1, 2), "tuple-key")
    assert m.get("zzz") is None
    assert m.get("zzz", 0) == 0
    assert (1, 2) in m and "zzz" not in m


def test_t02_remove():
    m = load("t02_hash_map").HashMap()
    m.put("a", 1)
    assert m.remove("a") == 1
    assert "a" not in m and len(m) == 0
    with pytest.raises(KeyError):
        m.remove("a")


def test_t02_equal_keys_are_one_key():
    m = load("t02_hash_map").HashMap()
    m.put(1, "int")
    m.put(1.0, "float")
    assert len(m) == 1 and m.get(True) == "float"


def test_t02_unhashable_key():
    m = load("t02_hash_map").HashMap()
    with pytest.raises(TypeError):
        m.put([1], "x")


class Collide:
    """Все экземпляры с одним хешем — гарантированная коллизия."""

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, Collide) and self.name == other.name


def test_t02_collisions():
    m = load("t02_hash_map").HashMap()
    keys = [Collide(c) for c in "abcde"]
    for i, k in enumerate(keys):
        m.put(k, i)
    assert [m.get(Collide(c)) for c in "abcde"] == [0, 1, 2, 3, 4]
    assert m.remove(Collide("c")) == 2
    assert Collide("c") not in m and len(m) == 4


def test_t02_resize():
    m = load("t02_hash_map").HashMap()
    assert len(m._buckets) == 8
    for i in range(6):
        m.put(f"k{i}", i)
    assert len(m._buckets) == 8, "6 пар = 0.75 × 8 — ещё не растём"
    m.put("k6", 6)
    assert len(m._buckets) == 16, "7 > 0.75 × 8 — корзин должно стать 16"
    for i in range(1000):
        m.put(i, i * i)
    assert all(m.get(i) == i * i for i in range(1000))
    assert all(m.get(f"k{i}") == i for i in range(7))
    assert len(m) == 1007
    assert len(m._buckets) >= 1007 / 0.75


def test_t02_no_builtin_dict():
    source = inspect.getsource(load("t02_hash_map"))
    for banned in ("dict(", "set(", "defaultdict", "{}", "Counter"):
        assert banned not in source, f"без встроенных dict/set: нашёл {banned!r}"


# ---------- t03 ----------
def test_t03_example():
    first = [{"id": 3}, {"id": 1}, {"id": 2}, {"id": 3}]
    second = [{"id": 2}, {"id": 3}, {"id": 9}]
    assert load("t03_common_users").common_users(first, second) == [3, 2]


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ([], [{"id": 1}], []),
        ([{"id": 1}], [], []),
        ([{"id": 1}, {"id": 2}], [{"id": 3}], []),
        ([{"id": 1}, {"id": 1}], [{"id": 1}, {"id": 1}], [1]),
        ([{"id": 5, "name": "a"}], [{"id": 5, "name": "b"}], [5]),
    ],
)
def test_t03_cases(first, second, expected):
    assert load("t03_common_users").common_users(first, second) == expected


def test_t03_linear():
    first = [{"id": i} for i in range(20_000)]
    second = [{"id": i} for i in range(10_000, 30_000)]
    result, spent = timed(load("t03_common_users").common_users, first, second)
    assert result == list(range(10_000, 20_000))
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n·m)"


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("text", "k", "expected"),
    [
        ("b a b a c", 2, [("a", 2), ("b", 2)]),
        ("The cat. the CAT, the dog!", 2, [("the", 3), ("cat", 2)]),
        ("", 3, []),
        ("one", 5, [("one", 1)]),
        ("x y", 0, []),
        ("x y", -1, []),
        ("Ёж ёж\nЁЖ, кот", 1, [("ёж", 3)]),
        ("z y x", 3, [("x", 1), ("y", 1), ("z", 1)]),
        ("api v2 api-v2 v2", 2, [("v2", 3), ("api", 2)]),
    ],
)
def test_t04_top_words(text, k, expected):
    assert load("t04_top_words").top_words(text, k) == expected


# ---------- t05 ----------
def test_t05_example():
    orders = [{"id": 1, "status": "NEW"}, {"id": 2, "status": "FILLED"}, {"id": 3, "status": "NEW"}]
    result = load("t05_group_orders").group_orders(orders)
    assert result == {"NEW": [1, 3], "FILLED": [2]}
    assert list(result) == ["NEW", "FILLED"]


def test_t05_plain_dict_and_empty():
    module = load("t05_group_orders")
    assert type(module.group_orders([{"id": 1, "status": "NEW"}])) is dict
    assert module.group_orders([]) == {}


def test_t05_input_untouched_and_lists_independent():
    orders = [{"id": 1, "status": "A"}, {"id": 2, "status": "B"}]
    snapshot = [dict(o) for o in orders]
    result = load("t05_group_orders").group_orders(orders)
    result["A"].append(99)
    assert result["B"] == [2], "у каждого статуса должен быть свой список"
    assert orders == snapshot


# ---------- t06 ----------
def test_t06_example():
    r = load("t06_recent_events").RecentEvents(3)
    for e in ["e1", "e2", "e3", "e4"]:
        r.add(e)
    assert r.items() == ["e2", "e3", "e4"]
    assert len(r) == 3 and r.total == 4


def test_t06_not_full_and_copy():
    r = load("t06_recent_events").RecentEvents(5)
    r.add("a")
    snapshot = r.items()
    snapshot.append("hack")
    assert r.items() == ["a"] and len(r) == 1 and r.total == 1


@pytest.mark.parametrize("n", [0, -1])
def test_t06_bad_n(n):
    with pytest.raises(ValueError):
        load("t06_recent_events").RecentEvents(n)


def test_t06_long_stream():
    r = load("t06_recent_events").RecentEvents(3)
    start = time.perf_counter()
    for i in range(200_000):
        r.add(i)
    assert time.perf_counter() - start < 1.0
    assert r.items() == [199_997, 199_998, 199_999] and r.total == 200_000


# ---------- t07 ----------
def names(records):
    return [r["name"] for r in records]


def test_t07_example():
    records = [
        {"name": "bob", "amount": "9.50"},
        {"name": "Ann", "amount": "100.00"},
        {"name": "cat", "amount": None},
        {"name": "dan", "amount": "100"},
        {"name": "Abe", "amount": None},
    ]
    snapshot = [dict(r) for r in records]
    assert names(load("t07_sort_records").sort_records(records)) == ["Ann", "dan", "bob", "Abe", "cat"]
    assert records == snapshot, "исходный список менять нельзя"


@pytest.mark.parametrize(
    ("records", "expected"),
    [
        ([], []),
        ([{"name": "a", "amount": "9"}, {"name": "b", "amount": "10"}], ["b", "a"]),
        ([{"name": "b", "amount": "0.10"}, {"name": "A", "amount": "0.1"}], ["A", "b"]),
        ([{"name": "x", "amount": "-5"}, {"name": "y", "amount": "0"}], ["y", "x"]),
        ([{"name": "z", "amount": None}, {"name": "a", "amount": "1"}], ["a", "z"]),
    ],
)
def test_t07_cases(records, expected):
    assert names(load("t07_sort_records").sort_records(records)) == expected

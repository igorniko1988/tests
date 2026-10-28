import copy
import importlib
import os

import pytest

SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(f"{SRC}.{name}")


# ---------- t01 ----------
def test_t01_calls_are_independent():
    add_tag = load("t01_fix_default").add_tag
    assert add_tag("smoke") == ["smoke"]
    assert add_tag("api") == ["api"]


def test_t01_own_list_is_mutated_and_returned():
    add_tag = load("t01_fix_default").add_tag
    mine = ["ui"]
    result = add_tag("x", mine)
    assert result is mine
    assert mine == ["ui", "x"]


def test_t01_empty_list_passed_is_used():
    add_tag = load("t01_fix_default").add_tag
    mine = []
    assert add_tag("x", mine) is mine


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("rows", "cols", "fill", "expected"),
    [
        (2, 3, 0, [[0, 0, 0], [0, 0, 0]]),
        (2, 2, ".", [[".", "."], [".", "."]]),
        (0, 5, 0, []),
        (3, 0, 0, [[], [], []]),
    ],
)
def test_t02_shape(rows, cols, fill, expected):
    assert load("t02_make_grid").make_grid(rows, cols, fill) == expected


def test_t02_rows_are_independent():
    grid = load("t02_make_grid").make_grid(3, 3)
    grid[0][0] = 1
    assert grid == [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert len({id(row) for row in grid}) == 3


def test_t02_default_fill():
    assert load("t02_make_grid").make_grid(1, 2) == [[0, 0]]


# ---------- t03 ----------
def test_t03_relation():
    relation = load("t03_relation").relation
    x = [1]
    assert relation(x, x) == "same"
    assert relation([1], [1]) == "equal"
    assert relation([1], [2]) == "different"
    assert relation(None, None) == "same"
    assert relation({"a": 1}, {"a": 1}) == "equal"
    assert relation(1, 1.0) == "equal"


# ---------- t04 ----------
ORDER = {"symbol": "BTC/USDT", "side": "buy", "meta": {"tags": ["smoke"]}}


def test_t04_changes_applied():
    template = copy.deepcopy(ORDER)
    p = load("t04_build_payload").build_payload(template, side="sell", qty="0.1")
    assert p == {"symbol": "BTC/USDT", "side": "sell", "meta": {"tags": ["smoke"]}, "qty": "0.1"}
    assert template == ORDER


def test_t04_template_untouched_after_nested_change():
    template = copy.deepcopy(ORDER)
    p = load("t04_build_payload").build_payload(template)
    assert p is not template
    p["meta"]["tags"].append("x")
    assert template["meta"]["tags"] == ["smoke"]


def test_t04_change_value_not_shared():
    template = {"items": []}
    tags = ["a"]
    p = load("t04_build_payload").build_payload(template, tags=tags)
    p["tags"].append("b")
    assert tags == ["a"]


# ---------- t05 ----------
def test_t05_example():
    base = {"api": {"url": "http://x", "timeout": 5}, "tags": ["a"]}
    override = {"api": {"timeout": 10}, "debug": True}
    snapshot = copy.deepcopy((base, override))
    result = load("t05_deep_merge").deep_merge(base, override)
    assert result == {"api": {"url": "http://x", "timeout": 10}, "tags": ["a"], "debug": True}
    assert (base, override) == snapshot


def test_t05_non_dict_replaces_dict_and_back():
    deep_merge = load("t05_deep_merge").deep_merge
    assert deep_merge({"a": {"x": 1}}, {"a": 5}) == {"a": 5}
    assert deep_merge({"a": 5}, {"a": {"x": 1}}) == {"a": {"x": 1}}


def test_t05_deep_levels():
    base = {"a": {"b": {"c": 1, "d": 2}}}
    override = {"a": {"b": {"d": 3, "e": 4}}}
    assert load("t05_deep_merge").deep_merge(base, override) == {"a": {"b": {"c": 1, "d": 3, "e": 4}}}


def test_t05_result_shares_nothing():
    base = {"tags": ["a"], "api": {"h": ["x"]}}
    override = {"extra": ["e"], "api": {"q": [1]}}
    result = load("t05_deep_merge").deep_merge(base, override)
    result["tags"].append("b")
    result["api"]["h"].append("y")
    result["extra"].append("f")
    result["api"]["q"].append(2)
    assert base == {"tags": ["a"], "api": {"h": ["x"]}}
    assert override == {"extra": ["e"], "api": {"q": [1]}}


def test_t05_empty():
    deep_merge = load("t05_deep_merge").deep_merge
    assert deep_merge({}, {}) == {}
    assert deep_merge({"a": 1}, {}) == {"a": 1}


# ---------- t06 ----------
def test_t06_freeze():
    freeze = load("t06_freeze").freeze
    assert freeze([1, [2, 3]]) == (1, (2, 3))
    assert freeze({"a": [1]}) == freeze({"a": [1]})
    assert freeze({"a": 1, "b": 2}) == freeze({"b": 2, "a": 1})
    assert freeze([1, 2]) != freeze([2, 1])
    assert freeze({1, 2}) == freeze({2, 1})
    assert freeze("abc") == "abc"
    assert freeze(None) is None
    hash(freeze({"x": {"y": [1, {2}]}, "z": (1, [2])}))


def test_t06_list_and_dict_differ():
    freeze = load("t06_freeze").freeze
    assert freeze({"a": 1}) != freeze([("a", 1)])


# ---------- t07 ----------
@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([3, 1, 3, 2, 1], [3, 1, 2]),
        ([{"id": 1}, {"id": 2}, {"id": 1}], [{"id": 1}, {"id": 2}]),
        ([[1, 2], [1, 2], [2, 1]], [[1, 2], [2, 1]]),
        ([], []),
        (["a"], ["a"]),
        ([{"a": 1, "b": 2}, {"b": 2, "a": 1}], [{"a": 1, "b": 2}]),
    ],
)
def test_t07_dedupe(items, expected):
    assert load("t07_dedupe").dedupe(items) == expected


def test_t07_returns_original_objects():
    first = {"id": 1}
    result = load("t07_dedupe").dedupe([first, {"id": 1}])
    assert result[0] is first


def test_t07_linear_enough():
    items = [{"id": i % 1000} for i in range(20000)]
    assert len(load("t07_dedupe").dedupe(items)) == 1000


# ---------- t08 ----------
def test_t08_deepcopy():
    my_deepcopy = load("t08_my_deepcopy").my_deepcopy
    src = {"a": [1, {"b": [2]}], "c": (3, [4]), "s": {1, 2}}
    dst = my_deepcopy(src)
    assert dst == src
    assert dst is not src
    assert dst["a"] is not src["a"]
    assert dst["a"][1] is not src["a"][1]
    assert dst["c"][1] is not src["c"][1]
    assert dst["s"] is not src["s"]
    dst["a"][1]["b"].append(99)
    dst["c"][1].append(5)
    assert src == {"a": [1, {"b": [2]}], "c": (3, [4]), "s": {1, 2}}


def test_t08_scalars():
    my_deepcopy = load("t08_my_deepcopy").my_deepcopy
    for value in (1, 1.5, "s", True, None):
        assert my_deepcopy(value) == value
    assert type(my_deepcopy((1, 2))) is tuple


# ---------- t09 ----------
def test_t09_self_reference():
    deepcopy_cycles = load("t09_deepcopy_cycles").deepcopy_cycles
    a = [1]
    a.append(a)
    b = deepcopy_cycles(a)
    assert b is not a
    assert b[1] is b
    assert b[0] == 1


def test_t09_shared_object_stays_shared():
    deepcopy_cycles = load("t09_deepcopy_cycles").deepcopy_cycles
    shared = [0]
    dst = deepcopy_cycles([shared, shared])
    assert dst[0] is dst[1]
    assert dst[0] is not shared


def test_t09_dict_cycle():
    deepcopy_cycles = load("t09_deepcopy_cycles").deepcopy_cycles
    d = {"name": "root", "children": []}
    d["children"].append({"parent": d})
    c = deepcopy_cycles(d)
    assert c is not d
    assert c["children"][0]["parent"] is c


def test_t09_plain_nested():
    deepcopy_cycles = load("t09_deepcopy_cycles").deepcopy_cycles
    src = {"a": [1, [2]]}
    dst = deepcopy_cycles(src)
    dst["a"][1].append(3)
    assert src == {"a": [1, [2]]}


# ---------- t10 ----------
def test_t10_snapshot():
    rec = load("t10_call_recorder").CallRecorder()
    payload = {"qty": 1}
    rec(payload, retry=True)
    payload["qty"] = 5
    assert rec.calls == [(({"qty": 1},), {"retry": True})]
    assert rec.last == (({"qty": 1},), {"retry": True})
    assert rec.count == 1


def test_t10_empty():
    rec = load("t10_call_recorder").CallRecorder()
    assert rec.calls == []
    assert rec.last is None
    assert rec.count == 0


def test_t10_history_cannot_be_spoiled_from_outside():
    rec = load("t10_call_recorder").CallRecorder()
    rec([1], k={"a": 1})
    calls = rec.calls
    calls.clear()
    assert rec.count == 1
    rec.calls[0][0][0].append(2)
    rec.calls[0][1]["k"]["a"] = 99
    rec.last[0][0].append(3)
    assert rec.calls == [(([1],), {"k": {"a": 1}})]


def test_t10_several_calls_order():
    rec = load("t10_call_recorder").CallRecorder()
    rec(1)
    rec(2, x=3)
    assert rec.calls == [((1,), {}), ((2,), {"x": 3})]
    assert rec.last == ((2,), {"x": 3})
    assert rec.count == 2

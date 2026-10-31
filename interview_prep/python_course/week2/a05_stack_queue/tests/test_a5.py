import importlib
import inspect
import os
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")
TIME_LIMIT = 1.0  # секунды; O(n²) на этих размерах не укладывается


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [("()[]{}", True), ("([]{})", True), ("(]", False), ("([)]", False), ("((", False), ("", True), ("())", False), ("]", False)],
)
def test_t01_valid_parentheses(s, expected):
    assert load("t01_valid_parentheses").valid_parentheses(s) is expected


# ---------- t02 ----------
def test_t02_min_stack():
    s = load("t02_min_stack").MinStack()
    s.push(5)
    s.push(2)
    s.push(7)
    s.push(2)
    assert len(s) == 4 and s.get_min() == 2 and s.top() == 2
    assert s.pop() == 2
    assert s.get_min() == 2
    assert s.pop() == 7
    assert s.pop() == 2
    assert s.get_min() == 5 and len(s) == 1


def test_t02_empty_raises():
    s = load("t02_min_stack").MinStack()
    for method in (s.pop, s.top, s.get_min):
        with pytest.raises(IndexError):
            method()


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("temps", "expected"),
    [
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([30, 30], [0, 0]),
        ([], []),
    ],
)
def test_t03_daily_temperatures(temps, expected):
    assert load("t03_daily_temperatures").daily_temperatures(temps) == expected


def test_t03_linear():
    temps = list(range(100_000, 0, -1)) + [200_000]
    result, spent = timed(load("t03_daily_temperatures").daily_temperatures, temps)
    assert result[0] == 100_000 and result[-1] == 0
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        (["2", "1", "+", "3", "*"], 9),
        (["4", "13", "5", "/", "+"], 6),
        (["7", "-2", "/"], -3),
        (["42"], 42),
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
        (["3", "5", "-"], -2),
    ],
)
def test_t04_eval_rpn(tokens, expected):
    assert load("t04_eval_rpn").eval_rpn(tokens) == expected


# ---------- t05 ----------
def test_t05_fifo():
    q = load("t05_queue_two_stacks").MyQueue()
    q.push(1)
    q.push(2)
    assert q.peek() == 1 and len(q) == 2
    assert q.pop() == 1
    q.push(3)
    assert [q.pop(), q.pop()] == [2, 3]
    assert len(q) == 0
    with pytest.raises(IndexError):
        q.pop()
    with pytest.raises(IndexError):
        q.peek()


def test_t05_amortized():
    q = load("t05_queue_two_stacks").MyQueue()
    start = time.perf_counter()
    for i in range(200_000):
        q.push(i)
        if i % 2:
            q.pop()
    assert q.peek() == 100_000
    assert time.perf_counter() - start < TIME_LIMIT


def test_t05_only_stack_operations():
    source = inspect.getsource(load("t05_queue_two_stacks").MyQueue)
    for banned in ("pop(0)", "insert(", "deque", "popleft"):
        assert banned not in source, f"нельзя использовать {banned}"


# ---------- t06 ----------
@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/home/", "/home"),
        ("/a/./b/../../c/", "/c"),
        ("/../", "/"),
        ("/home//foo/", "/home/foo"),
        ("/.../a/../b", "/.../b"),
        ("/", "/"),
    ],
)
def test_t06_simplify_path(path, expected):
    assert load("t06_simplify_path").simplify_path(path) == expected


# ---------- t07 ★ ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [([2, 1, 2, 4, 3], [4, 2, 4, -1, -1]), ([5, 4, 3], [-1, -1, -1]), ([], []), ([1, 3, 2, 4], [3, 4, 4, -1])],
)
def test_t07_next_greater(nums, expected):
    assert load("t07_next_greater").next_greater(nums) == expected


# ---------- t08 ★ ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("3[a]2[bc]", "aaabcbc"),
        ("3[a2[c]]", "accaccacc"),
        ("2[abc]3[cd]ef", "abcabccdcdcdef"),
        ("10[x]", "x" * 10),
        ("abc", "abc"),
    ],
)
def test_t08_decode_string(s, expected):
    assert load("t08_decode_string").decode_string(s) == expected


# ---------- t09 ★ ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [("abbaca", "ca"), ("azxxzy", "ay"), ("aa", ""), ("abc", "abc"), ("", "")],
)
def test_t09_remove_adjacent(s, expected):
    assert load("t09_remove_adjacent").remove_adjacent(s) == expected


# ---------- t10 ★ ----------
@pytest.mark.parametrize(
    ("heights", "expected"),
    [([2, 1, 5, 6, 2, 3], 10), ([2, 4], 4), ([], 0), ([3, 3, 3], 9), ([1], 1)],
)
def test_t10_largest_rectangle(heights, expected):
    assert load("t10_largest_rectangle").largest_rectangle(heights) == expected


def test_t10_linear():
    heights = list(range(1, 100_001))
    result, spent = timed(load("t10_largest_rectangle").largest_rectangle, heights)
    assert result == 2_500_050_000
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"

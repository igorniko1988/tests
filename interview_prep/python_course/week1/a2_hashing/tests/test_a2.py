import importlib
import inspect
import os
import random
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")
TIME_LIMIT = 0.5  # секунды; O(n²) на этих размерах не укладывается


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
        ([-1, -2, -3, -4, -5], -8, [2, 4]),
        ([0, 4, 3, 0], 0, [0, 3]),
    ],
)
def test_t01_two_sum(nums, target, expected):
    assert load("t01_two_sum").two_sum(nums, target) == expected


def test_t01_linear():
    nums = list(range(100_000))
    result, spent = timed(load("t01_two_sum").two_sum, nums, 199_997)
    assert result == [99_998, 99_999]
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("listen", "silent", True),
        ("rat", "car", False),
        ("aab", "abb", False),
        ("", "", True),
        ("ab", "a", False),
        ("Ab", "ab", False),
    ],
)
def test_t02_is_anagram(a, b, expected):
    assert load("t02_is_anagram").is_anagram(a, b) is expected


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["eat", "tea", "tan", "ate", "nat", "bat"], [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
        ([""], [[""]]),
        ([], []),
        (["ab", "ba", "abc"], [["ab", "ba"], ["abc"]]),
    ],
)
def test_t03_group_anagrams(words, expected):
    assert load("t03_group_anagrams").group_anagrams(words) == expected


def test_t03_returns_plain_lists():
    result = load("t03_group_anagrams").group_anagrams(["a", "a"])
    assert type(result) is list and all(type(group) is list for group in result)


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("abcba", "b"),
        ("abca", "a"),
        ("abc", None),
        ("", None),
        ("aA", None),
        ("xx", "x"),
    ],
)
def test_t04_first_repeated(s, expected):
    assert load("t04_first_repeated").first_repeated(s) == expected


# ---------- t05 ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([1, 2, 3, 1], 3, True),
        ([1, 0, 1, 1], 1, True),
        ([1, 2, 3, 1, 2, 3], 2, False),
        ([], 0, False),
        ([1, 1], 0, False),
        ([5, 1, 5, 9, 5], 1, False),
    ],
)
def test_t05_nearby_duplicate(nums, k, expected):
    assert load("t05_nearby_duplicate").nearby_duplicate(nums, k) is expected


def test_t05_linear():
    nums = list(range(100_000))
    result, spent = timed(load("t05_nearby_duplicate").nearby_duplicate, nums, 100_000)
    assert result is False
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n·k)"


# ---------- t06 ----------
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([1, 2, 2, 3], 3),
        ([], 0),
        ([5], 1),
        ([-1, 0, 1, 10], 3),
    ],
)
def test_t06_longest_consecutive(nums, expected):
    assert load("t06_longest_consecutive").longest_consecutive(nums) == expected


def test_t06_no_sort():
    source = inspect.getsource(load("t06_longest_consecutive").longest_consecutive)
    assert "sort" not in source, "сортировать нельзя по условию"


def test_t06_linear():
    nums = list(range(200_000))
    random.Random(1).shuffle(nums)
    result, spent = timed(load("t06_longest_consecutive").longest_consecutive, nums)
    assert result == 200_000
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t07 ★ ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1, -1, 0], 0, 3),
        ([], 0, 0),
        ([3], 3, 1),
    ],
)
def test_t07_subarray_sum(nums, k, expected):
    assert load("t07_subarray_sum").subarray_sum(nums, k) == expected


def test_t07_linear():
    nums = [1] * 20_000
    result, spent = timed(load("t07_subarray_sum").subarray_sum, nums, 10_000)
    assert result == 10_001
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t08 ★ ----------
@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [
        ("egg", "add", True),
        ("foo", "bar", False),
        ("badc", "baba", False),
        ("", "", True),
        ("paper", "title", True),
        ("ab", "a", False),
    ],
)
def test_t08_is_isomorphic(s, t, expected):
    assert load("t08_is_isomorphic").is_isomorphic(s, t) is expected


# ---------- t09 ★ ----------
@pytest.mark.parametrize(
    ("pattern", "s", "expected"),
    [
        ("abba", "dog cat cat dog", True),
        ("abba", "dog cat cat fish", False),
        ("aaaa", "dog cat cat dog", False),
        ("abba", "dog dog dog dog", False),
        ("ab", "dog", False),
    ],
)
def test_t09_word_pattern(pattern, s, expected):
    assert load("t09_word_pattern").word_pattern(pattern, s) is expected


# ---------- t10 ★ ----------
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([1, 2, 2, 1], [2, 2], [2, 2]),
        ([4, 9, 5], [9, 4, 9, 8, 4], [4, 9]),
        ([1, 1, 1], [1], [1]),
        ([], [1], []),
        ([3, 1, 3], [3, 3, 3], [3, 3]),
    ],
)
def test_t10_intersect_counts(a, b, expected):
    assert load("t10_intersect_counts").intersect_counts(a, b) == expected

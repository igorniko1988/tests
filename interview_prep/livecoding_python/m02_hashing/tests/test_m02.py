"""Тесты модуля 2. Одна задача: uv run pytest -k t04"""
import importlib
import inspect
import os
import random
import time

import pytest

SRC = os.environ.get("SRC", "tasks")   # SRC=solutions — проверить эталон


def load(module, name):
    return getattr(importlib.import_module(f"{SRC}.{module}"), name)


def body(module, name):
    """Код функции без строки def — для проверок «без sort»."""
    src = inspect.getsource(load(module, name))
    assert "NotImplementedError" not in src, "задача ещё не решена"
    return src.split("\n", 1)[1]


def fast(fn, *args, limit=0.3):
    t = time.perf_counter()
    result = fn(*args)
    assert time.perf_counter() - t < limit, "похоже на O(n^2), нужно O(n)"
    return result


@pytest.mark.parametrize("nums,expected", [
    ([1, 2, 3, 1], True), ([1, 2, 3, 4], False), ([], False),
    ([7], False), ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
])
def test_t01_contains_duplicate(nums, expected):
    assert load("t01_contains_duplicate", "contains_duplicate")(nums) is expected


def test_t01_linear_time():
    nums = list(range(5000))
    assert fast(load("t01_contains_duplicate", "contains_duplicate"), nums) is False


@pytest.mark.parametrize("s,expected", [
    ("leetcode", 0), ("loveleetcode", 2), ("aabb", -1), ("", -1), ("z", 0), ("aabbc", 4),
])
def test_t02_first_unique_char(s, expected):
    assert load("t02_first_unique_char", "first_unique_char")(s) == expected


@pytest.mark.parametrize("s,t,expected", [
    ("anagram", "nagaram", True), ("rat", "car", False), ("aab", "abb", False),
    ("", "", True), ("a", "ab", False), ("listen", "silent", True),
])
def test_t03_valid_anagram(s, t, expected):
    assert load("t03_valid_anagram", "is_anagram")(s, t) is expected


@pytest.mark.parametrize("nums,target,expected", [
    ([2, 7, 11, 15], 9, [0, 1]), ([3, 2, 4], 6, [1, 2]), ([3, 3], 6, [0, 1]),
    ([-1, -2, -3, -4, -5], -8, [2, 4]), ([0, 4, 3, 0], 0, [0, 3]),
])
def test_t04_two_sum(nums, target, expected):
    assert load("t04_two_sum", "two_sum")(nums, target) == expected


def test_t04_linear_time():
    nums = list(range(5000))
    assert fast(load("t04_two_sum", "two_sum"), nums, 9997) == [4998, 4999]


def norm_groups(groups):
    return sorted(sorted(g) for g in groups)


@pytest.mark.parametrize("strs,expected", [
    (["eat", "tea", "tan", "ate", "nat", "bat"], [["ate", "eat", "tea"], ["nat", "tan"], ["bat"]]),
    ([""], [[""]]), (["a"], [["a"]]), ([], []), (["ab", "ba", "abc"], [["ab", "ba"], ["abc"]]),
])
def test_t05_group_anagrams(strs, expected):
    assert norm_groups(load("t05_group_anagrams", "group_anagrams")(strs)) == norm_groups(expected)


@pytest.mark.parametrize("a,b,expected", [
    ([1, 2, 2, 1], [2, 2], [2, 2]), ([4, 9, 5], [9, 4, 9, 8, 4], [4, 9]),
    ([1, 2], [3], []), ([], [1], []), ([1, 1, 1], [1, 1], [1, 1]),
])
def test_t06_intersect(a, b, expected):
    assert sorted(load("t06_intersect", "intersect")(a, b)) == expected


@pytest.mark.parametrize("note,magazine,expected", [
    ("a", "b", False), ("aa", "ab", False), ("aa", "aab", True),
    ("", "abc", True), ("abc", "", False), ("aab", "baa", True),
])
def test_t07_ransom_note(note, magazine, expected):
    assert load("t07_ransom_note", "can_construct")(note, magazine) is expected


@pytest.mark.parametrize("s,t,expected", [
    ("egg", "add", True), ("foo", "bar", False), ("badc", "baba", False),
    ("paper", "title", True), ("", "", True), ("ab", "aa", False),
])
def test_t08_isomorphic(s, t, expected):
    assert load("t08_isomorphic", "is_isomorphic")(s, t) is expected


@pytest.mark.parametrize("nums,k,expected", [
    ([1, 1, 1, 2, 2, 3], 2, [1, 2]), ([1], 1, [1]), ([4, 4, 5, 5, 5, 6], 1, [5]),
    ([-1, -1, 2, 2, 2, 3], 2, [-1, 2]), ([5, 6, 7], 3, [5, 6, 7]),
])
def test_t09_top_k_frequent(nums, k, expected):
    assert sorted(load("t09_top_k_frequent", "top_k_frequent")(nums, k)) == expected


@pytest.mark.parametrize("nums,expected", [
    ([100, 4, 200, 1, 3, 2], 4), ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
    ([], 0), ([1, 2, 0, 1], 3), ([5], 1), ([-2, -1, 0, 10], 3),
])
def test_t10_longest_consecutive(nums, expected):
    assert load("t10_longest_consecutive", "longest_consecutive")(nums) == expected


def test_t10_no_sort():
    src = body("t10_longest_consecutive", "longest_consecutive")
    assert "sorted" not in src and ".sort" not in src, "сортировать нельзя, нужно O(n)"


def test_t10_linear_time():
    nums = list(range(20000))
    random.Random(1).shuffle(nums)
    assert fast(load("t10_longest_consecutive", "longest_consecutive"), nums) == 20000

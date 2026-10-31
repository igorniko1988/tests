import importlib
import os
import random
import string
import time

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")
TIME_LIMIT = 1.0  # секунды; O(n·k) и O(n²) на этих размерах не укладываются


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


def random_text(n, alphabet=string.ascii_lowercase, seed=1):
    rnd = random.Random(seed)
    return "".join(rnd.choice(alphabet) for _ in range(n))


# ---------- t01 ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [([2, 1, 5, 1, 3, 2], 3, 9), ([-1, -2, -3], 2, -3), ([1, 2], 3, None), ([5], 1, 5), ([1, 2], 0, None)],
)
def test_t01_max_sum_k(nums, k, expected):
    assert load("t01_max_sum_k").max_sum_k(nums, k) == expected


def test_t01_linear():
    nums = list(range(200_000))
    result, spent = timed(load("t01_max_sum_k").max_sum_k, nums, 1000)
    assert result == sum(range(199_000, 200_000))
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n·k)"


# ---------- t02 ----------
@pytest.mark.parametrize(
    ("s", "expected"),
    [("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0), ("abba", 2), ("dvdf", 3)],
)
def test_t02_longest_unique(s, expected):
    assert load("t02_longest_unique").longest_unique(s) == expected


def test_t02_linear():
    s = random_text(200_000)
    result, spent = timed(load("t02_longest_unique").longest_unique, s)
    assert 1 <= result <= 26
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t03 ----------
@pytest.mark.parametrize(
    ("target", "nums", "expected"),
    [(7, [2, 3, 1, 2, 4, 3], 2), (4, [1, 4, 4], 1), (11, [1, 1, 1, 1], 0), (15, [1, 2, 3, 4, 5], 5), (1, [], 0)],
)
def test_t03_min_subarray_len(target, nums, expected):
    assert load("t03_min_subarray_len").min_subarray_len(target, nums) == expected


def test_t03_linear():
    nums = [1] * 200_000
    result, spent = timed(load("t03_min_subarray_len").min_subarray_len, 100_000, nums)
    assert result == 100_000
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t04 ----------
@pytest.mark.parametrize(
    ("pattern", "text", "expected"),
    [("ab", "eidbaooo", True), ("ab", "eidboaoo", False), ("", "abc", True), ("abc", "ab", False), ("adc", "dcda", True)],
)
def test_t04_has_permutation(pattern, text, expected):
    assert load("t04_has_permutation").has_permutation(pattern, text) is expected


def test_t04_linear():
    text = random_text(100_000, "abc")
    pattern = "d" * 500
    result, spent = timed(load("t04_has_permutation").has_permutation, pattern, text)
    assert result is False
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n·k)"


# ---------- t05 ----------
@pytest.mark.parametrize(
    ("s", "k", "expected"),
    [("ABAB", 2, 4), ("AABABBA", 1, 4), ("", 2, 0), ("ABC", 0, 1), ("AAAA", 0, 4)],
)
def test_t05_character_replacement(s, k, expected):
    assert load("t05_character_replacement").character_replacement(s, k) == expected


def test_t05_linear():
    s = random_text(100_000, "AB")
    _, spent = timed(load("t05_character_replacement").character_replacement, s, 50)
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n²)"


# ---------- t06 ----------
@pytest.mark.parametrize(
    ("text", "pattern", "expected"),
    [("cbaebabacd", "abc", [0, 6]), ("abab", "ab", [0, 1, 2]), ("a", "ab", []), ("aaa", "a", [0, 1, 2])],
)
def test_t06_find_anagrams(text, pattern, expected):
    assert load("t06_find_anagrams").find_anagrams(text, pattern) == expected


def test_t06_linear():
    text = random_text(100_000, "ab")
    _, spent = timed(load("t06_find_anagrams").find_anagrams, text, "ab" * 250)
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n·k)"


# ---------- t07 ★ ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]), ([4], 1, [4]), ([9, 8, 7], 2, [9, 8]), ([1, 2, 3], 3, [3])],
)
def test_t07_window_max(nums, k, expected):
    assert load("t07_window_max").window_max(nums, k) == expected


def test_t07_linear():
    nums = list(range(200_000, 0, -1))
    result, spent = timed(load("t07_window_max").window_max, nums, 10_000)
    assert result[0] == 200_000 and len(result) == 190_001
    assert spent < TIME_LIMIT, f"{spent:.2f} с — похоже на O(n·k)"


# ---------- t08 ★ ----------
@pytest.mark.parametrize(
    ("s", "k", "expected"),
    [("eceba", 2, 3), ("aa", 1, 2), ("abc", 0, 0), ("abaccc", 2, 4), ("", 3, 0)],
)
def test_t08_longest_k_distinct(s, k, expected):
    assert load("t08_longest_k_distinct").longest_k_distinct(s, k) == expected


# ---------- t09 ★ ----------
@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [("ADOBECODEBANC", "ABC", "BANC"), ("a", "a", "a"), ("a", "aa", ""), ("ab", "b", "b"), ("abcab", "ab", "ab")],
)
def test_t09_min_window(s, t, expected):
    assert load("t09_min_window").min_window(s, t) == expected


# ---------- t10 ★ ----------
@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [([10, 5, 2, 6], 100, 8), ([1, 2, 3], 0, 0), ([1, 1, 1], 2, 6), ([100], 100, 0)],
)
def test_t10_product_less_k(nums, k, expected):
    assert load("t10_product_less_k").product_less_k(nums, k) == expected

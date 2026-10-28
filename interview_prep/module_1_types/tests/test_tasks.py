import pytest

from tasks.task_01_default_args import f
from tasks.task_02_first_unique import first_unique
from tasks.task_03_palindrome import is_palindrome
from tasks.task_04_anagram import is_anagram
from tasks.task_05_top_words import top_words
from tasks.task_06_dedupe import dedupe, dedupe_dicts
from tasks.task_07_second_largest import second_largest
from tasks.task_08_two_sum import two_sum


def test_task_01_default_args():
    assert f(1) == [1]
    assert f(2) == [2]
    assert f(3, []) == [3]
    assert f(4) == [4]


def test_task_01_does_not_use_mutable_default():
    assert f.__defaults__ is None or all(
        not isinstance(d, (list, dict, set)) for d in f.__defaults__
    )


@pytest.mark.parametrize("s,expected", [
    ("swiss", "w"), ("aabb", None), ("", None), ("a", "a"), ("aabbc", "c"),
])
def test_task_02_first_unique(s, expected):
    assert first_unique(s) == expected


@pytest.mark.parametrize("s,expected", [
    ("A man, a plan, a canal: Panama", True),
    ("race a car", False), ("", True), ("a", True), ("No 'x' in Nixon", True),
])
def test_task_03_palindrome(s, expected):
    assert is_palindrome(s) is expected


@pytest.mark.parametrize("a,b,expected", [
    ("listen", "silent", True), ("Dormitory", "dirty room", True),
    ("aab", "abb", False), ("abc", "abcd", False), ("", "", True),
])
def test_task_04_anagram(a, b, expected):
    assert is_anagram(a, b) is expected


def test_task_05_top_words():
    text = "the cat and the dog and the bird"
    assert top_words(text) == [("the", 3), ("and", 2), ("cat", 1)]


def test_task_05_case_and_punctuation():
    assert top_words("Hi, hi! HI. bye", 2) == [("hi", 3), ("bye", 1)]


def test_task_06_dedupe():
    assert dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert dedupe([]) == []
    assert dedupe(["a", "a"]) == ["a"]


def test_task_06_dedupe_does_not_mutate_input():
    src = [1, 1, 2]
    dedupe(src)
    assert src == [1, 1, 2]


def test_task_06_dedupe_dicts():
    items = [{"id": 1, "n": "a"}, {"id": 2, "n": "b"}, {"id": 1, "n": "c"}]
    assert dedupe_dicts(items, "id") == [{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]


@pytest.mark.parametrize("nums,expected", [
    ([1, 5, 3], 3), ([5, 5, 4], 4), ([5, 5], None), ([], None), ([-1, -5], -5),
])
def test_task_07_second_largest(nums, expected):
    assert second_largest(nums) == expected


@pytest.mark.parametrize("nums,target,expected", [
    ([2, 7, 11, 15], 9, (0, 1)), ([3, 2, 4], 6, (1, 2)),
    ([3, 3], 6, (0, 1)), ([1, 2], 10, None),
])
def test_task_08_two_sum(nums, target, expected):
    assert two_sum(nums, target) == expected

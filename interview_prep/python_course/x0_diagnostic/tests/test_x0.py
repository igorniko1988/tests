import importlib
import os

import pytest

SRC = os.environ.get("SRC", "tasks")
t01 = importlib.import_module(f"{SRC}.t01_first_unique")
t02 = importlib.import_module(f"{SRC}.t02_error_report")


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("leetcode", 0),
        ("loveleetcode", 2),
        ("aabb", -1),
        ("", -1),
        ("z", 0),
        ("aA", 0),
        ("aab", 2),
        ("abcabcd", 6),
    ],
)
def test_t01_first_unique(s, expected):
    assert t01.first_unique(s) == expected


LOG = [
    "2026-10-28T10:00:00 ERROR orders Timeout to price-feed",
    "2026-10-28T10:00:01 INFO orders Created 42",
    "2026-10-28T10:00:02 ERROR auth Bad token",
    "2026-10-28T10:00:03 ERROR orders Insufficient funds",
    "",
]


def test_t02_example():
    assert t02.error_report(LOG) == [("orders", 2), ("auth", 1)]


def test_t02_empty():
    assert t02.error_report([]) == []


def test_t02_no_errors():
    assert t02.error_report(["2026-10-28T10:00:01 INFO orders Created 42"]) == []


def test_t02_skips_broken_lines():
    lines = ["garbage", "2026-10-28T10:00:00 ERROR", "   ", "2026-10-28T10:00:00 ERROR ws Closed"]
    assert t02.error_report(lines) == [("ws", 1)]


def test_t02_tie_sorted_by_name_and_top():
    lines = [
        "t ERROR b x",
        "t ERROR a x",
        "t ERROR c x",
        "t ERROR d x",
        "t ERROR d y",
    ]
    assert t02.error_report(lines) == [("d", 2), ("a", 1), ("b", 1)]
    assert t02.error_report(lines, top=1) == [("d", 2)]


def test_t02_level_is_exact():
    lines = ["t error a x", "t ERRORS a x", "t WARN ERROR x"]
    assert t02.error_report(lines) == []

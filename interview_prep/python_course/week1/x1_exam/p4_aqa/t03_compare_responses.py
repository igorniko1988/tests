"""X1 t03 (AQA, 20 min). Compare expected and actual API records.

A test gets a list of records from an API and compares it with the expected
list. Records are dicts with a unique "id" in expected. Return:

    {"missing": [...], "extra": [...], "mismatched": [...], "duplicated": [...]}

- missing - ids that are in expected but not in actual;
- extra - ids that are in actual but not in expected;
- mismatched - ids present in both, but the records are not equal (==);
- duplicated - ids that appear more than once in actual;
- every list is sorted ascending, each id once.
For mismatched, compare the FIRST actual record with that id.

Example:
    expected = [{"id": 1, "s": "NEW"}, {"id": 2, "s": "NEW"}, {"id": 3, "s": "NEW"}]
    actual   = [{"id": 2, "s": "FILLED"}, {"id": 3, "s": "NEW"}, {"id": 4, "s": "NEW"},
                {"id": 3, "s": "NEW"}]
    compare_responses(expected, actual)
        -> {"missing": [1], "extra": [4], "mismatched": [2], "duplicated": [3]}

Follow-up questions:
- Why is a dict "id -> record" better than searching the list each time?
- Which bug in an API does "duplicated" catch? (Hint: pagination.)

Run (from interview_prep/python_course/week1/x1_exam): uv run pytest -k t03
"""


def compare_responses(expected: list[dict], actual: list[dict]) -> dict[str, list[int]]:
    raise NotImplementedError

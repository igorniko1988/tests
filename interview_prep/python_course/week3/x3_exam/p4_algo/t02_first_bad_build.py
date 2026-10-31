"""X3 t02 (algorithm, part of 40 min). First bad build (git bisect).

Builds are numbered 1..n. At some build a bug was introduced: every build from it on is bad.
is_bad(build) runs the test suite on a build (it is slow!). Return the first bad build,
or -1 if all builds are good.

Requirements:
- O(log n) calls of is_bad. The test counts calls: n = 1_000_000 must use at most 21 calls.

Examples:
    first_bad_build(5, lambda b: b >= 4)   -> 4
    first_bad_build(1, lambda b: True)     -> 1
    first_bad_build(3, lambda b: False)    -> -1

Follow-up questions:
- How does git bisect use exactly this idea?

Run (from interview_prep/python_course/week3/x3_exam): uv run pytest -k t02
"""


def first_bad_build(n: int, is_bad) -> int:
    raise NotImplementedError

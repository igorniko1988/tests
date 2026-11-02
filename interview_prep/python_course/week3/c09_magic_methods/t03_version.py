"""C9 t03 (required, ~20 min). Compare version strings.

Implement a class Version(text) for versions like "1.10.0", "2.0", "1.9.3":
- compare numerically part by part; missing trailing parts count as 0,
  so Version("1.2") == Version("1.2.0");
- support ==, <, <=, >, >= (you may use functools.total_ordering);
- sorted(["1.10.0", "1.9.3", "1.2"], key=Version) -> ["1.2", "1.9.3", "1.10.0"];
- hashable consistently with == (Version("1.2") and Version("1.2.0") are one element in a set);
- str(v) returns the original text; repr(v) -> "Version('1.10.0')";
- invalid text ("1.x", "", "1..2") -> ValueError.

Follow-up questions:
- Why is "1.10" < "1.9" True for strings?
- How did you make 1.2 and 1.2.0 equal AND have the same hash?

Run (from interview_prep/python_course/week3/c09_magic_methods): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 3.
"""


class Version:
    def __init__(self, text: str) -> None:
        raise NotImplementedError

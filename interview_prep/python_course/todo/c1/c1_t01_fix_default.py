"""C1 t01 (required, ~5 min). Fix the mutable default argument.

This helper is used across the test framework, and tags from one test leak into another:

    def add_tag(tag, tags=[]):
        tags.append(tag)
        return tags

    add_tag("smoke")  -> ["smoke"]
    add_tag("api")    -> ["smoke", "api"]   # bug: expected ["api"]

Fix it so that:
- every call WITHOUT a list gets its own new empty list;
- if a list IS passed, append to that same list and return it
  (an empty list [] passed by the caller counts as "passed").

Examples:
    add_tag("smoke")       -> ["smoke"]
    add_tag("api")         -> ["api"]
    mine = ["ui"]
    add_tag("x", mine)     -> ["ui", "x"]   # and mine is ["ui", "x"] too

Follow-up questions:
- Why does the original version share one list between calls?
- Why would `if not tags:` be wrong instead of `if tags is None:`?

Run (from interview_prep/python_course/todo): uv run pytest -k c1_t01
Теория: interview_prep/python_course/c01_objects/s07_default_arg/THEORY.md, раздел 7.
"""


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

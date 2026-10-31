"""A5 t06 (required, ~20 min). Simplify a Unix path.

Given an absolute Unix path, return its canonical form:
- "." means the current directory, ".." - the parent (at the root it stays at root);
- several slashes count as one; no trailing slash (except the root "/").
Any other name, including "...", is a regular directory name.

Examples:
    simplify_path("/home/")                 -> "/home"
    simplify_path("/a/./b/../../c/")        -> "/c"
    simplify_path("/../")                   -> "/"
    simplify_path("/home//foo/")            -> "/home/foo"
    simplify_path("/.../a/../b")            -> "/.../b"

Follow-up questions:
- Why is a stack the natural structure here?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 4.
"""


def simplify_path(path: str) -> str:
    raise NotImplementedError

"""C3 t03 (required, ~10 min). Common users.

You get two API responses, each is a list of users: [{"id": 1, ...}, ...].
Return the ids that appear in BOTH lists.

Requirements:
- Keep the order of the first list (by first occurrence).
- No duplicates in the result.
- Time complexity O(n + m). Tests use lists of 20 000 users each.

Example:
    first  = [{"id": 3}, {"id": 1}, {"id": 2}, {"id": 3}]
    second = [{"id": 2}, {"id": 3}, {"id": 9}]
    common_users(first, second) -> [3, 2]

    common_users([], [{"id": 1}]) -> []

Follow-up questions:
- Why doesn't set(a) & set(b) satisfy the requirements?
- What is the complexity of a nested-loop solution?

Run: uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 4.
"""


def common_users(first: list[dict], second: list[dict]) -> list[int]:
    raise NotImplementedError

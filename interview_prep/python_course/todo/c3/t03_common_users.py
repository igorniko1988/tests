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

Run (from interview_prep/python_course/todo): uv run pytest tests/test_c3.py -k t03
Теория: interview_prep/python_course/c03_collections/s04_set/THEORY.md, раздел 4.
"""


def common_users(first: list[dict], second_idssecond: list[dict]) -> list[int]:
    second_ids = {user['id'] for user in second_idssecond}
    seen = set()
    result = []
    for user in first:
        id = user['id']
        if id in second_ids and id not in seen:
            result.append(id)
            seen.add(id)

    return result

first  = [{"id": 3}, {"id": 1}, {"id": 2}, {"id": 3}]
second = [{"id": 2}, {"id": 3}, {"id": 9}]

print(common_users(first, second))
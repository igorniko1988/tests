"""A0 t04 (required, ~15 min). Common ids - optimize O(n * m) to O(n + m).

Given two lists of ids a and b (e.g. orders from the API and from the database),
return the ids present in BOTH lists.

Requirements:
- Keep the order of a (by first occurrence).
- Each id appears in the result once, even if it repeats in a or b.
- Do not modify the input.

Examples:
    common_ids([3, 1, 2], [2, 3])  -> [3, 2]
    common_ids([1, 1, 2], [1])     -> [1]
    common_ids([1, 2], [3, 4])     -> []
    common_ids([], [1])            -> []

The code below is a working brute-force solution. It hides two O(n) list
lookups: `x in b` and `x not in result`. Rewrite it in O(n + m).

Follow-up questions:
- Why not just return list(set(a) & set(b))?
- What is the memory complexity of your solution?

Run (from interview_prep/python_course/todo): uv run pytest tests/test_a0.py -k t04
Теория: interview_prep/python_course/a00_big_o/s07_method/THEORY.md и interview_prep/python_course/a00_big_o/s04_hidden_cost/THEORY.md.
"""


def common_ids(a: list, b: list) -> list:
    result = []
    for x in a:
        if x in b and x not in result:
            result.append(x)
    return result

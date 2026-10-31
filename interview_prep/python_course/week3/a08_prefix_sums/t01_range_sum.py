"""A8 t01 (required, ~15 min). Range sum query.

Implement a class RangeSum(nums) answering many queries:
- query(l, r) -> sum of nums[l..r] INCLUSIVE, in O(1);
- l > r or indices out of range -> IndexError.

Requirements:
- Precompute in O(n). Tests make 200 000 queries on 100 000 numbers.
- Changing the original list after creation must not affect answers.

Example:
    rs = RangeSum([-2, 0, 3, -5, 2, -1])
    rs.query(0, 2)  -> 1
    rs.query(2, 5)  -> -1
    rs.query(0, 5)  -> -3

Follow-up questions:
- Why the extra 0 at the start of the prefix list?

Run (from interview_prep/python_course/week3/a08_prefix_sums): uv run pytest -k t01
Теория: THEORY.md в этой папке, раздел 1.
"""


class RangeSum:
    def __init__(self, nums: list[int]) -> None:
        raise NotImplementedError

    def query(self, l: int, r: int) -> int:
        raise NotImplementedError

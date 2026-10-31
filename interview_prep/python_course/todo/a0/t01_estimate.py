"""A0 t01 (required, ~20 min). Estimate the complexity.

For each of the 10 functions below, write its worst-case time and EXTRA memory
complexity in ANSWERS as "O(time) / O(memory)", e.g. "O(n) / O(1)".

Rules:
- n is the input length; with two inputs a and b use n = len(a), m = len(b):
  "O(n*m)" or "O(n + m)".
- Memory is only what the function allocates itself (the input does not count).
  The recursion stack DOES count.
- Squares: O(n^2), O(n²) or O(n*n); logs: O(log n), O(n log n).
- Pass mark: 8 of 10 on the first try.

Follow-up questions:
- Which "O(1)-looking" lines are actually O(n) here?

Run (from interview_prep/python_course/todo): uv run python a0/t01_estimate.py
Теория: interview_prep/python_course/a00_big_o/s04_hidden_cost/THEORY.md, s03_python_ops/THEORY.md, s05_memory/THEORY.md.
"""

from collections import Counter


# f1
def total(prices):
    result = 0
    for p in prices:
        result += p
    return result


# f2
def has_dup(items):
    seen = []
    for x in items:
        if x in seen:
            return True
        seen.append(x)
    return False


# f3
def first_unique(s):
    for i, ch in enumerate(s):
        if s.count(ch) == 1:
            return i
    return -1


# f4
def first_unique_fast(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


# f5
def drain(queue):
    total = 0
    while queue:
        total += queue.pop(0)
    return total


# f6
def contains(sorted_nums, target):
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == target:
            return True
        if sorted_nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


# f7
def spread(nums):
    ordered = sorted(nums)
    return ordered[-1] - ordered[0]


# f8
def squares(nums):
    result = []
    for x in nums:
        result = result + [x * x]
    return result


# f9
def rec_sum(nums):
    if not nums:
        return 0
    return nums[0] + rec_sum(nums[1:])


# f10
def matches(a, b):
    count = 0
    for x in a:
        for y in b:
            if x == y:
                count += 1
    return count


# ============================ ТВОИ ОТВЕТЫ ============================
# "O(время) / O(память)"

ANSWERS = {
    "f1": "",
    "f2": "",
    "f3": "",
    "f4": "",
    "f5": "",
    "f6": "",
    "f7": "",
    "f8": "",
    "f9": "",
    "f10": "",
}


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run_estimate

    # ключ ответов лежит в уроке: a00_big_o/solutions/estimate_key.py
    lesson_file = Path(__file__).resolve().parents[2] / "a00_big_o" / "s04_hidden_cost" / "t01_estimate.py"
    run_estimate(ANSWERS, str(lesson_file))

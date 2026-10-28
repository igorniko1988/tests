"""t01 (разминка, 5 мин). Contains Duplicate — LeetCode 217.

Верни True, если в списке есть хотя бы одно повторяющееся число.
Нужно O(n): без цикла в цикле и без сортировки.

contains_duplicate([1, 2, 3, 1])  -> True
contains_duplicate([1, 2, 3, 4])  -> False
contains_duplicate([])            -> False

Вопрос интервьюера: а если нельзя тратить память?
"""


def contains_duplicate(nums: list[int]) -> bool:
    seen = set()

    for n in nums:
        if n in seen:
            return True
        else:
            seen.add(n)
    return False

print(contains_duplicate([1, 2, 3, 4]))

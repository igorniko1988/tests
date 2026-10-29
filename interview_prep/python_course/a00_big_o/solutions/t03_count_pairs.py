from collections import Counter


def count_pairs(nums: list[int], target: int) -> int:
    seen = Counter()  # число → сколько раз встречалось ЛЕВЕЕ текущего
    count = 0
    for x in nums:
        count += seen[target - x]  # каждая встреченная «пара» даёт по одной паре с x
        seen[x] += 1  # после подсчёта — чтобы не сложить x с самим собой
    return count


# [3, 3, 3], 6: x=3 → seen[3]=0; x=3 → +1 (с индексом 0); x=3 → +2 (с 0 и 1). Итого 3.
# Время O(n), память O(n).

from collections import defaultdict


def subarray_sum(nums: list[int], k: int) -> int:
    counts = defaultdict(int)
    counts[0] = 1  # пустой префикс
    prefix = total = 0
    for x in nums:
        prefix += x
        total += counts[prefix - k]
        counts[prefix] += 1
    return total

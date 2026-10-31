from collections import defaultdict


def subarray_sum_k(nums: list[int], k: int) -> int:
    seen = defaultdict(int)
    seen[0] = 1
    prefix = count = 0
    for x in nums:
        prefix += x
        count += seen[prefix - k]
        seen[prefix] += 1
    return count

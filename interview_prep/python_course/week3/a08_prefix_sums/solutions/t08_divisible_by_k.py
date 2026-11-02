from collections import defaultdict


def divisible_by_k(nums: list[int], k: int) -> int:
    seen = defaultdict(int)
    seen[0] = 1
    prefix = count = 0
    for x in nums:
        prefix = (prefix + x) % k
        count += seen[prefix]
        seen[prefix] += 1
    return count

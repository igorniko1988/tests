from collections import Counter


def pair_difference(nums: list[int], k: int) -> bool:
    if k == 0:
        return any(count > 1 for count in Counter(nums).values())
    values = set(nums)
    return any(x + k in values for x in values)

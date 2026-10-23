def two_sum(nums, target):
    seen = {}
    for j, n in enumerate(nums):
        i = seen.get(target - n)
        if i is not None:
            return (i, j)
        seen[n] = j
    return None

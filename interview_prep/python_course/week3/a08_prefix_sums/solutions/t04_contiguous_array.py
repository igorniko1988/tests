def contiguous_array(nums: list[int]) -> int:
    first = {0: -1}  # префикс -> первый индекс, где он встретился
    prefix = best = 0
    for i, x in enumerate(nums):
        prefix += 1 if x == 1 else -1
        if prefix in first:
            best = max(best, i - first[prefix])
        else:
            first[prefix] = i
    return best

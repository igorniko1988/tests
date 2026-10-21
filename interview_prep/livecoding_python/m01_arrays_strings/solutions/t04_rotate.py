def rotate(nums: list[int], k: int) -> list[int]:
    if not nums:
        return []
    k %= len(nums)          # сдвиг на len — это ноль сдвигов
    return nums[-k:] + nums[:-k] if k else nums[:]

# На месте за O(1): развернуть весь список, потом первые k и остальные.

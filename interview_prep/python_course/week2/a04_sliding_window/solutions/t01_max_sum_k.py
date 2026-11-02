def max_sum_k(nums: list[int], k: int) -> int | None:
    if k <= 0 or len(nums) < k:
        return None
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        best = max(best, window)
    return best

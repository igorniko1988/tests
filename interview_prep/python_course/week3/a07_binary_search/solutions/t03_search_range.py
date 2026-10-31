def search_range(nums: list[int], target: int) -> list[int]:
    def first_at_least(value: int) -> int:
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] >= value:
                hi = mid
            else:
                lo = mid + 1
        return lo

    start = first_at_least(target)
    if start == len(nums) or nums[start] != target:
        return [-1, -1]
    return [start, first_at_least(target + 1) - 1]

def rotate(nums: list[int], k: int) -> None:
    if not nums:
        return
    k %= len(nums)
    nums[:] = nums[-k:] + nums[:-k] if k else nums

def sorted_squares(nums: list[int]) -> list[int]:
    result = [0] * len(nums)
    left, right = 0, len(nums) - 1
    for pos in range(len(nums) - 1, -1, -1):
        if abs(nums[left]) > abs(nums[right]):
            result[pos] = nums[left] ** 2
            left += 1
        else:
            result[pos] = nums[right] ** 2
            right -= 1
    return result

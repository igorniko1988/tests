def running_sum(nums: list[int]) -> list[int]:
    result = []
    total = 0
    for x in nums:
        total += x
        result.append(total)
    return result

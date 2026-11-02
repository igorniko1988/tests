def product_except_self(nums: list[int]) -> list[int]:
    answer = [1] * len(nums)
    prefix = 1  # произведение всех слева от i
    for i in range(len(nums)):
        answer[i] = prefix
        prefix *= nums[i]
    suffix = 1  # произведение всех справа от i
    for i in range(len(nums) - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer

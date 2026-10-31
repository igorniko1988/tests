from collections import deque


def window_max(nums: list[int], k: int) -> list[int]:
    window = deque()  # индексы, значения по убыванию
    result = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()
        window.append(i)
        if window[0] <= i - k:
            window.popleft()
        if i >= k - 1:
            result.append(nums[window[0]])
    return result

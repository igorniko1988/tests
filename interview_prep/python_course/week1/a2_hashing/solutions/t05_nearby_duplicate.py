def nearby_duplicate(nums: list[int], k: int) -> bool:
    last = {}  # значение -> последний индекс
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False

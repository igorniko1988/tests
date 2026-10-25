def two_sum(nums: list[int], target: int) -> list[int]:
    # seen: число -> индекс. Для каждого x ищем «пару» target - x среди прошлых. O(n).
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []

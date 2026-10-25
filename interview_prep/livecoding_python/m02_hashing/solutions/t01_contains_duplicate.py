def contains_duplicate(nums: list[int]) -> bool:
    # set хранит только уникальные: если длина меньше — были дубли. O(n), O(n).
    return len(set(nums)) != len(nums)

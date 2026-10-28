def longest_consecutive(nums: list[int]) -> int:
    # Считаем цепочку только от её начала (x - 1 нет в set). Каждое число трогаем ~2 раза. O(n).
    num_set = set(nums)
    best = 0
    for x in num_set:
        if x - 1 not in num_set:
            length = 1
            while x + length in num_set:
                length += 1
            best = max(best, length)
    return best

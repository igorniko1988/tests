def missing_number(nums: list[int]) -> int:
    # Сумма 0..n по формуле минус фактическая сумма. Второй вариант — XOR.
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)

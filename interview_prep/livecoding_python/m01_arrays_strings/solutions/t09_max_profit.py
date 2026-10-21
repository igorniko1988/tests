def max_profit(prices: list[int]) -> int:
    # Идём слева направо, помним минимум «до сегодня». O(n), O(1).
    best = 0
    min_price = float("inf")
    for p in prices:
        min_price = min(min_price, p)
        best = max(best, p - min_price)
    return best

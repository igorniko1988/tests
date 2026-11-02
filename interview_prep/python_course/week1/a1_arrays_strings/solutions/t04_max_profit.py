def max_profit(prices: list[int]) -> int:
    best = 0
    lowest = None
    for price in prices:
        if lowest is None or price < lowest:
            lowest = price
        elif price - lowest > best:
            best = price - lowest
    return best

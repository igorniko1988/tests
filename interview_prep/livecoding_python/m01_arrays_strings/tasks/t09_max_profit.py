"""t09 ★ (сложная, 15 мин). Best Time to Buy and Sell Stock — LeetCode 121.

prices[i] — цена в день i. Купи один раз и продай один раз позже.
Верни максимальную прибыль, если прибыли нет — 0.
Решение «в лоб» за O(n^2) расскажи вслух, а напиши за O(n).

max_profit([7, 1, 5, 3, 6, 4])  -> 5   # купить за 1, продать за 6
max_profit([7, 6, 4, 3, 1])     -> 0
max_profit([])                  -> 0
"""


def max_profit(prices: list[int]) -> int:
    prices_at_days = {}
    profits = []

    for day in range(len(prices)):
        for price in prices:
            buy = price
            best_sell = max(prices[day:])
            profit = best_sell - price
            profits.append(profit)
            prices_at_days[day] = profits

    print(prices_at_days)
    best_proposals = {day: max(price) for day, price in prices_at_days.items() }




    return best_proposals



print(max_profit([7, 1, 5, 3, 6, 4]))

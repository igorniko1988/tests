from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    # Корзины: buckets[f] — числа, которые встретились f раз. O(n).
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in counts.items():
        buckets[freq].append(num)
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    return result

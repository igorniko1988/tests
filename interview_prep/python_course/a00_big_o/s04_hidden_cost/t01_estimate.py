"""A0 t01 «Оцени сложность» — 10 фрагментов, для каждого время и память.

Теория: THEORY.md в этой папке (скрытая сложность), ../s03_python_ops/THEORY.md (цены операций),
../s05_memory/THEORY.md (память).

КАК ОТВЕЧАТЬ
В ANSWERS внизу впиши для каждого фрагмента строку «O(время) / O(память)», например "O(n) / O(1)".
- n — длина входа; если входов два (a и b) — n = len(a), m = len(b): "O(n·m)" или "O(n + m)".
- Память — только ДОПОЛНИТЕЛЬНАЯ: то, что функция создала сама (вход не считается).
  Стек рекурсии считается!
- Квадрат можно писать O(n^2), O(n²) или O(n*n); логарифм — O(log n), O(n log n).
- Худший случай.

Проверка (из папки a00_big_o):  uv run python s04_hidden_cost/t01_estimate.py
Скрипт сверит и объяснит каждый ответ. Зачёт: 8 из 10 с первой попытки.
"""

from collections import Counter


# f1
def total(prices):
    result = 0
    for p in prices:
        result += p
    return result


# f2
def has_dup(items):
    seen = []
    for x in items:
        if x in seen:
            return True
        seen.append(x)
    return False


# f3
def first_unique(s):
    for i, ch in enumerate(s):
        if s.count(ch) == 1:
            return i
    return -1


# f4
def first_unique_fast(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


# f5
def drain(queue):
    total = 0
    while queue:
        total += queue.pop(0)
    return total


# f6
def contains(sorted_nums, target):
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == target:
            return True
        if sorted_nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


# f7
def spread(nums):
    ordered = sorted(nums)
    return ordered[-1] - ordered[0]


# f8
def squares(nums):
    result = []
    for x in nums:
        result = result + [x * x]
    return result


# f9
def rec_sum(nums):
    if not nums:
        return 0
    return nums[0] + rec_sum(nums[1:])


# f10
def matches(a, b):
    count = 0
    for x in a:
        for y in b:
            if x == y:
                count += 1
    return count


# ============================ ТВОИ ОТВЕТЫ ============================
# "O(время) / O(память)"

ANSWERS = {
    "f1": "",
    "f2": "",
    "f3": "",
    "f4": "",
    "f5": "",
    "f6": "",
    "f7": "",
    "f8": "",
    "f9": "",
    "f10": "",
}


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run_estimate

    run_estimate(ANSWERS, __file__)

"""Модуль 1. Big-O, списки и строки, идиомы Python.

Запуск: uv run python lesson.py
Читай сверху вниз. Перед каждым блоком «ЧТО ВЫВЕДЕТ?» сначала ответь сам,
потом смотри вывод.
"""
import time


def part(title):
    print(f"\n=== {title} ===")


# ---------------------------------------------------------------------------
part("1. Big-O: зачем это спрашивают")
# Big-O — как растёт время работы, когда вход растёт.
# Интервьюер почти всегда спрашивает: «Какая сложность? Можно быстрее?»
#
#   O(1)        — не зависит от размера: dict[key], list[i], append
#   O(log n)    — делим пополам: бинарный поиск
#   O(n)        — один проход: for x in nums
#   O(n log n)  — сортировка: sorted(nums)
#   O(n^2)      — цикл в цикле: каждую пару
#
# Проверим на практике: поиск в list — O(n), в set — O(1).

data_list = list(range(1_000_000))
data_set = set(data_list)

t = time.perf_counter()
for _ in range(100):
    999_999 in data_list
print(f"in list: {time.perf_counter() - t:.4f} c")

t = time.perf_counter()
for _ in range(100):
    999_999 in data_set
print(f"in set:  {time.perf_counter() - t:.6f} c")
# Разница в тысячи раз. Это главный приём оптимизации на собесе:
# «вместо поиска в списке кладу в set/dict».


# ---------------------------------------------------------------------------
part("2. Стоимость операций со списком")
# list — это массив. Конец дешёвый, начало дорогое.
#   nums.append(x)     O(1)
#   nums.pop()         O(1)
#   nums.pop(0)        O(n)  — все элементы сдвигаются
#   nums.insert(0, x)  O(n)
#   x in nums          O(n)
#   nums[a:b]          O(b-a) — срез это КОПИЯ
#   nums.sort()        O(n log n), сортирует на месте, возвращает None
#   sorted(nums)       O(n log n), возвращает новый список

nums = [3, 1, 2]
result = nums.sort()
print("ЧТО ВЫВЕДЕТ? result =", result, "nums =", nums)
# result = None. Частая ошибка на собесе: return nums.sort()


# ---------------------------------------------------------------------------
part("3. Строки неизменяемые")
s = "hello"
# s[0] = "H"  -> TypeError: 'str' object does not support item assignment
s2 = "H" + s[1:]
print(s2)

# Склейка в цикле через += на каждом шаге может копировать строку.
# Идиома: собрать части в список и один раз сделать join. Это O(n).
parts = []
for ch in "abc":
    parts.append(ch.upper())
print("".join(parts))

# Нужно менять символы по индексу? Переведи в список и обратно.
chars = list("hello")
chars[0] = "J"
print("".join(chars))


# ---------------------------------------------------------------------------
part("4. Срезы")
a = [0, 1, 2, 3, 4, 5]
print(a[1:4])    # [1, 2, 3]   — конец не включается
print(a[:2])     # [0, 1]
print(a[-2:])    # [4, 5]      — два последних
print(a[::-1])   # разворот
print(a[::2])    # каждый второй
print("ЧТО ВЫВЕДЕТ?", a[10:], a[-100:2])
# [] и [0, 1]: срез за границами не падает, а индекс падает (a[10] -> IndexError)


# ---------------------------------------------------------------------------
part("5. Обход: enumerate, zip, reversed, range")
names = ["ann", "bob", "eve"]
for i, name in enumerate(names):
    print(i, name)

ages = [30, 25]
print(list(zip(names, ages)))   # zip останавливается на самом коротком

for i in range(len(names) - 1, -1, -1):   # индексы с конца: 2, 1, 0
    print("с конца:", names[i])

print(list(reversed(names)))

# Соседние пары — частая конструкция
nums = [1, 4, 9, 16]
print([b - a for a, b in zip(nums, nums[1:])])   # [3, 5, 7]


# ---------------------------------------------------------------------------
part("6. Обмен значений и несколько присваиваний")
x, y = 1, 2
x, y = y, x
print(x, y)

nums = [10, 20, 30]
i, j = 0, 2
nums[i], nums[j] = nums[j], nums[i]
print(nums)   # [30, 20, 10] — так меняют элементы в два указателя


# ---------------------------------------------------------------------------
part("7. Полезные методы строк")
print("  hi  there ".split())      # ['hi', 'there'] — без аргумента режет по любым пробелам
print("a,b,,c".split(","))         # ['a', 'b', '', 'c']
print("Hello".lower(), "a1!".isalnum(), "7".isdigit(), "abc".isalpha())
print("abc".startswith("ab"), "  x ".strip())
print(ord("a"), chr(98))           # 97 b — код символа и обратно
print("ЧТО ВЫВЕДЕТ?", "   ".split(), "".split(","))
# [] и [''] — разное поведение split с аргументом и без


# ---------------------------------------------------------------------------
part("8. min, max, sum, any, all с генератором")
nums = [3, -1, 7]
print(max(nums), min(nums), sum(nums))
print(max(["bb", "a", "ccc"], key=len))     # ccc
print(any(n < 0 for n in nums), all(n > -5 for n in nums))
print(max([], default=None))               # без default на пустом — ValueError
print(float("inf") > 10**100)              # бесконечность как стартовое значение минимума


# ---------------------------------------------------------------------------
part("9. Изменение на месте против нового списка")
# «In-place» в условии значит: менять переданный список, память O(1),
# обычно вернуть None. Проверяется тем, что тест смотрит на тот же объект.


def bad(nums):
    nums = [n for n in nums if n]   # новое имя, внешний список не изменился


def good(nums):
    nums[:] = [n for n in nums if n]   # меняем содержимое того же объекта


a = [0, 1, 0, 2]
bad(a)
print("после bad:", a)
good(a)
print("после good:", a)
# nums[:] = ... быстро, но память O(n). Настоящий O(1) — два указателя (задача t03).


# ---------------------------------------------------------------------------
part("10. divmod, //, % — работа с цифрами")
print(divmod(17, 5))   # (3, 2)
n = 1234
digits = []
while n:
    n, d = divmod(n, 10)
    digits.append(d)
print(digits[::-1])    # [1, 2, 3, 4]
print("ЧТО ВЫВЕДЕТ?", -7 // 2, -7 % 2)
# -4 и 1: в Python // округляет вниз, а не к нулю

print("\nГотово. Переходи к tasks/t01_reverse_words.py")

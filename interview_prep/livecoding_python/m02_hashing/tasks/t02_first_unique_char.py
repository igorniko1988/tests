"""t02 (разминка, 7 мин). First Unique Character — LeetCode 387.

Верни индекс первой буквы, которая встречается в строке ровно один раз.
Если такой нет, верни -1.

first_unique_char("leetcode")      -> 0   ('l')
first_unique_char("loveleetcode")  -> 2   ('v')
first_unique_char("aabb")          -> -1
first_unique_char("")              -> -1
"""


def first_unique_char(s: str) -> int:
    for index, char in enumerate(s):
        if s.count(char) == 1:
            return index
    return -1

print(first_unique_char("aabb"))

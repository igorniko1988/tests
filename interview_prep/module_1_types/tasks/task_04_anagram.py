"""Задача 4. Анаграммы.

Две строки анаграммы, если состоят из тех же букв в другом порядке.
Регистр и пробелы игнорируем.

is_anagram("listen", "silent") -> True
is_anagram("Dormitory", "dirty room") -> True
is_anagram("aab", "abb") -> False

Реши двумя способами и скажи, какой лучше и почему (sorted и Counter).

Проверка: pytest -k task_04 -q
"""


def is_anagram(a, b):
    first_word, second_word = a, b
    first_word = ''.join((ch.lower() for ch in first_word if ch.isalnum()))
    second_word = ''.join((ch.lower() for ch in first_word if ch.isalnum()))

    return sorted(first_word) == sorted(second_word)

print(is_anagram("aab", "abb"))
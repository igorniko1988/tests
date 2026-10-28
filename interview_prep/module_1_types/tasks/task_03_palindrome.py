"""Задача 3. Палиндром.

Игнорируем регистр, пробелы и знаки препинания (оставляем только буквы и цифры).

is_palindrome("A man, a plan, a canal: Panama") -> True
is_palindrome("race a car") -> False
is_palindrome("") -> True

Проверка: pytest -k task_03 -q
"""


def is_palindrome(s: str):
    edited_string = ''.join(ch.lower() for ch in s if ch.isalnum())
    print(edited_string)
    return edited_string == edited_string[::-1]

print(is_palindrome("A man, a plan, a canal: Panama"))

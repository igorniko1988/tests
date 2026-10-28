"""t01 (разминка, 5 мин). Reverse Words in a String — LeetCode 151.

Разверни порядок слов. Слова разделены одним или несколькими пробелами,
в начале и в конце могут быть пробелы. В ответе слова через один пробел.

reverse_words("the sky is blue")    -> "blue is sky the"
reverse_words("  hello   world  ")  -> "world hello"
reverse_words("   ")                -> ""

Сложность: O(n) время.
"""


def reverse_words(s: str) -> str:
    edited_words = []
    word = ''
    for ch in s:
        if ' ' in ch:
            if word:
                edited_words.append(word)
                word = ''
        else:
            word +=ch
    edited_words.append(word)

    result = ''

    for word in edited_words[::-1]:
        if result:
            result += ' ' + str(word)
        else:
            result += str(word)
    return result

print(reverse_words("the sky is blue"))


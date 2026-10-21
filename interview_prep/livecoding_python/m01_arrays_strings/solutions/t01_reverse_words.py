def reverse_words(s: str) -> str:
    # split() без аргумента сам убирает лишние пробелы. O(n) время и память.
    return " ".join(reversed(s.split()))

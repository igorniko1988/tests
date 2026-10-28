from collections import Counter


def is_anagram(a, b):
    def norm(s):
        return Counter(c.lower() for c in s if not c.isspace())
    return norm(a) == norm(b)

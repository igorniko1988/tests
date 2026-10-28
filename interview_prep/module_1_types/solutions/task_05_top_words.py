import re
from collections import Counter


def top_words(text, n=3):
    words = re.findall(r"[a-z']+", text.lower())
    return Counter(words).most_common(n)

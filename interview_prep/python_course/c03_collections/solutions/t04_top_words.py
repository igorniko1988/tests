import re
from collections import Counter


def top_words(text: str, k: int) -> list[tuple[str, int]]:
    if k <= 0:
        return []
    counts = Counter(re.findall(r"\w+", text.lower()))
    # most_common на ничьей держит порядок появления, поэтому сортируем сами
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]

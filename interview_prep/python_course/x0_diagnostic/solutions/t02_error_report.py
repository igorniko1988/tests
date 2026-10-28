from collections import Counter


def error_report(lines: list[str], top: int = 3) -> list[tuple[str, int]]:
    counts = Counter()
    for line in lines:
        parts = line.split(maxsplit=3)
        if len(parts) < 4:
            continue
        _, level, service, _ = parts
        if level == "ERROR":
            counts[service] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:top]

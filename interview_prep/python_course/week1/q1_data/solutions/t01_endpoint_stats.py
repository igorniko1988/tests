def endpoint_stats(lines: list[str]) -> dict[str, dict[str, int]]:
    stats = {}
    for line in lines:
        parts = line.split()
        if len(parts) != 4 or not parts[2].isdigit():
            continue
        path, status = parts[1], int(parts[2])
        entry = stats.setdefault(path, {"count": 0, "errors": 0})
        entry["count"] += 1
        if status >= 500:
            entry["errors"] += 1
    return stats

def can_attend(meetings: list[list[int]]) -> bool:
    ordered = sorted(meetings)
    return all(ordered[i][0] >= ordered[i - 1][1] for i in range(1, len(ordered)))

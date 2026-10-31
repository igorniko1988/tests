def insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    result = []
    start, end = new
    i = 0
    while i < len(intervals) and intervals[i][1] < start:  # целиком левее
        result.append(list(intervals[i]))
        i += 1
    while i < len(intervals) and intervals[i][0] <= end:  # пересекаются — сливаем
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])
    result.extend(list(iv) for iv in intervals[i:])  # целиком правее
    return result

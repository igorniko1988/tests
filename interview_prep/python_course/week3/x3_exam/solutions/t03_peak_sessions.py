def peak_sessions(sessions: list[list[int]]) -> tuple:
    events = []
    for start, end in sessions:
        events.append((start, 1))
        events.append((end, -1))
    events.sort()  # при равном времени -1 (конец) раньше +1 (начала)
    active = peak = 0
    moment = None
    for time, delta in events:
        active += delta
        if active > peak:
            peak, moment = active, time
    return peak, moment

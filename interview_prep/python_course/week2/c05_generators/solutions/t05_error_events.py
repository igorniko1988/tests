def parse(lines):
    for line in lines:
        parts = line.split(maxsplit=3)
        if len(parts) < 4:
            continue
        ts, level, service, msg = parts
        yield {"ts": ts, "level": level, "service": service, "msg": msg}


def only(events, level):
    return (event for event in events if event["level"] == level)


def error_events(lines):
    return only(parse(lines), "ERROR")

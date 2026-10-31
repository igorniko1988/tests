def filter_log(lines, level=None, request_id=None):
    for number, line in enumerate(lines, start=1):
        parts = line.split(maxsplit=3)
        if len(parts) < 4:
            continue
        if level is not None and parts[1] != level:
            continue
        if request_id is not None and parts[2] != request_id:
            continue
        yield number, line

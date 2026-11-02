def group_consecutive(iterable, key=None):
    get_key = key or (lambda item: item)
    group, current = [], None
    for item in iterable:
        k = get_key(item)
        if group and k != current:
            yield current, group
            group = []
        current = k
        group.append(item)
    if group:
        yield current, group

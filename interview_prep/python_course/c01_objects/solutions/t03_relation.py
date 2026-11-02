def relation(a, b) -> str:
    if a is b:
        return "same"
    if a == b:
        return "equal"
    return "different"

def decode_string(s: str) -> str:
    stack = []  # (строка до "[", число повторов)
    current, number = "", 0
    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch == "[":
            stack.append((current, number))
            current, number = "", 0
        elif ch == "]":
            prefix, repeat = stack.pop()
            current = prefix + current * repeat
        else:
            current += ch
    return current

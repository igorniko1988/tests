def decode(s: str) -> str:
    parts = []
    char, digits = "", ""
    for ch in s:
        if ch.isdigit():
            digits += ch
        else:
            if char:
                parts.append(char * int(digits))
            char, digits = ch, ""
    if char:
        parts.append(char * int(digits))
    return "".join(parts)

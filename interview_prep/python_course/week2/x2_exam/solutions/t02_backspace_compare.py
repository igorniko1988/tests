def backspace_compare(s: str, t: str) -> bool:
    def typed(text: str) -> list[str]:
        stack = []
        for ch in text:
            if ch == "#":
                if stack:
                    stack.pop()
            else:
                stack.append(ch)
        return stack

    return typed(s) == typed(t)

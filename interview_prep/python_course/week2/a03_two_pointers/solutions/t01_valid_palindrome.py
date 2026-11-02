def valid_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].casefold() != s[right].casefold():
            return False
        else:
            left += 1
            right -= 1
    return True

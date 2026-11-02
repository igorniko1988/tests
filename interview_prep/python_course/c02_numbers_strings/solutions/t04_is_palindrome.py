def is_palindrome(s: str) -> bool:
    cleaned = [ch.casefold() for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]


# O(n) время, O(n) память. ★ O(1) памяти — два индекса с концов, пропуская не-буквы:
#
# def is_palindrome(s):
#     left, right = 0, len(s) - 1
#     while left < right:
#         if not s[left].isalnum():
#             left += 1
#         elif not s[right].isalnum():
#             right -= 1
#         elif s[left].casefold() != s[right].casefold():
#             return False
#         else:
#             left, right = left + 1, right - 1
#     return True

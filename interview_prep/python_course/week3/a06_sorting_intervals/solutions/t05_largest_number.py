from functools import cmp_to_key


def largest_number(nums: list[int]) -> str:
    parts = [str(n) for n in nums]
    parts.sort(key=cmp_to_key(lambda a, b: (b + a > a + b) - (b + a < a + b)))
    result = "".join(parts)
    return "0" if result.startswith("0") else result

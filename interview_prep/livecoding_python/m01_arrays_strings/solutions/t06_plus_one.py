def plus_one(digits: list[int]) -> list[int]:
    result = digits[:]
    for i in range(len(result) - 1, -1, -1):
        if result[i] < 9:
            result[i] += 1
            return result
        result[i] = 0       # 9 + 1 = 10: ставим 0, перенос идёт дальше
    return [1] + result     # все были девятки

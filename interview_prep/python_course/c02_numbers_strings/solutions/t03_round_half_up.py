def round_half_up(x: float, digits: int = 2) -> float:
    sign = -1 if x < 0 else 1
    text = repr(abs(x))  # кратчайшая запись: repr(2.675) == '2.675'
    whole, _, frac = text.partition(".")
    frac = frac.ljust(digits + 1, "0")  # чтобы была цифра после нужных знаков
    kept = int(whole + frac[:digits])  # 2.675, digits=2 → 267
    if frac[digits] >= "5":  # первая отброшенная цифра
        kept += 1  # → 268
    return sign * kept / 10**digits  # 268 / 100 → 2.68


# Почему не round(x * 100) / 100: 1.005 * 100 == 100.49999999999999 — ошибка float уже в
# умножении. Строка из repr — та запись, которую видит человек, её и округляем.

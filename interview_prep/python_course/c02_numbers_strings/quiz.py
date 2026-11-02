"""C2. «Что выведет» — 15 фрагментов на весь урок.

Правила:
1. Пиши ответ в ANSWERS внизу файла ДО запуска фрагмента.
2. Потом проверяй:  uv run python quiz.py 4      (один)
                    uv run python quiz.py all    (все подряд)
3. Если фрагмент падает, ответ — имя исключения (TypeError и т. п.).
4. Зачёт урока: не меньше 12 из 15 до запуска. Пиши в чат «готово C2 quiz».
"""

import sys

SNIPPETS = {
    1: """
print(-7 // 2, -7 % 2)
""",
    2: """
print(0.1 * 3 == 0.3)
""",
    3: """
print(round(0.5), round(1.5))
""",
    4: """
from decimal import Decimal
print(Decimal("1.1") + Decimal("2.2"))
""",
    5: """
from decimal import Decimal
print(Decimal(1.1) == Decimal("1.1"))
""",
    6: """
print("5" + "5", "5" * 2)
""",
    7: """
print("5" + 5)
""",
    8: """
print("Hello World".split("o"))
""",
    9: """
print(f"{10 / 3:.3f}")
""",
    10: """
print(len("ё"), len("ё".encode()))
""",
    11: """
print(bool("False"), bool(0.0))
""",
    12: """
print(1 == 1.0, hash(1) == hash(1.0))
""",
    13: """
x = None
print(x or [], x is None)
""",
    14: """
print(repr("abc"[5:]), "abc"[1:100])
""",
    15: """
print(10 / 4, 10 // 4, 10 % 4)
""",
}


def run(n: int) -> None:
    print(f"#{n}", SNIPPETS[n].rstrip(), "\n--- вывод ---", sep="")
    try:
        exec(SNIPPETS[n], {})
    except Exception as e:  # noqa: BLE001
        print(type(e).__name__ + ":", e)
    print()


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    for n in SNIPPETS if arg == "all" else [int(arg)]:
        run(n)


# ============================ ТВОИ ОТВЕТЫ ============================
# Пиши точный вывод (со скобками и кавычками) или имя исключения.
# Если строк вывода несколько — через " | ".

ANSWERS = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
    10: "",
    11: "",
    12: "",
    13: "",
    14: "",
    15: "",
}

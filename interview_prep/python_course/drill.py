"""Проверка упражнений «что выведет» (drills.py в папке каждого раздела).

Вызывается из drills.py раздела, отдельно не запускается.
Запускает каждый фрагмент, сравнивает вывод с ответом и показывает объяснение
из <урок>/solutions/drills_explain.py. Пока ответ пустой, правильный вывод не показывается.
"""

import contextlib
import importlib.util
import io
from pathlib import Path


def actual_output(code: str, setup: str = "") -> str:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(setup + "\n" + code, {"__name__": "__drill__"})
    except Exception as e:  # noqa: BLE001
        return " | ".join([*buf.getvalue().splitlines(), type(e).__name__])
    return " | ".join(buf.getvalue().splitlines())


def normalize(text: str) -> str:
    return " | ".join(part.strip() for part in text.strip().split("|"))


def loose(text: str) -> str:
    """Без пробелов, запятых и кавычек — чтобы отличить «не понял» от «не тот формат»."""
    return "".join(ch for ch in text if ch not in " ,'\"")


def load_solution(drills_file: str, name: str):
    # solutions/ ищем рядом с файлом (урок без разделов), потом уровнем выше (урок с разделами sNN_*)
    here = Path(drills_file).resolve()
    candidates = [base / "solutions" / f"{name}.py" for base in (here.parents[0], here.parents[1])]
    path = next((c for c in candidates if c.exists()), None)
    if path is None:
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_explain(drills_file: str) -> dict[str, str]:
    module = load_solution(drills_file, "drills_explain")
    return module.EXPLAIN if module else {}


def run(D: dict[str, str], A: dict[str, str], drills_file: str, setup: str = "", optional=()) -> None:
    """setup — общий код, который выполняется перед каждым фрагментом (например, класс-счётчик).
    optional — ключи дополнительных фрагментов («доп.»): их можно пропустить, раздел без них закрыт."""
    explain = load_explain(drills_file)
    # счёт отдельно для обязательных и дополнительных: [верно, ошибок, не отвечено]
    score = {False: [0, 0, 0], True: [0, 0, 0]}
    for key, code in D.items():
        extra = key in optional
        mark = " (доп.)" if extra else ""
        print(f"── {key}{mark} " + "─" * 50, code.rstrip(), sep="")
        mine = A.get(key, "").strip()
        if not mine:
            print(f"   ответ не вписан — заполни A[{key!r}]\n")
            score[extra][2] += 1
            continue
        real = actual_output(code, setup)
        ok = normalize(mine) == normalize(real)
        score[extra][0 if ok else 1] += 1
        print(f"   твой ответ: {mine}")
        print(f"   на деле:    {real}")
        if ok:
            print("   ✅ верно")
        elif loose(mine) == loose(real):
            print("   ⚠️ по смыслу верно, но формат вывода другой — сравни посимвольно")
        else:
            print("   ❌ ошибка")
        if key in explain:
            print("   почему:", explain[key])
        print()
    right, wrong, empty = score[False]
    print(f"Обязательные: верно {right}, ошибок {wrong}, не отвечено {empty}")
    if optional:
        right, wrong, empty = score[True]
        print(f"Доп. (по желанию): верно {right}, ошибок {wrong}, не отвечено {empty}")


def normalize_big_o(text: str) -> str:
    """O(n^2), O(n²), O(n**2), o(N*N) → одно и то же; O(n·m) == O(m*n)."""
    t = text.strip().lower().replace(" ", "")
    for a, b in (("**2", "²"), ("^2", "²"), ("n*n", "n²"), ("×", "*"), ("·", "*")):
        t = t.replace(a, b)
    t = t.replace("logn", "log(n)").replace("log₂n", "log(n)").replace("log2(n)", "log(n)")
    if t.startswith("o(") and t.endswith(")"):
        inner = t[2:-1].replace("*", "")
        if inner in ("nm", "mn"):
            inner = "nm"
        if inner in ("nlog(n)", "log(n)n"):
            inner = "nlog(n)"
        t = f"o({inner})"
    return t


def run_estimate(ANSWERS: dict[str, str], estimate_file: str) -> None:
    """Проверка оценок сложности: ответ «O(время) / O(память)» сверяется с solutions/estimate_key.py."""
    module = load_solution(estimate_file, "estimate_key")
    key, why = (module.KEY, module.WHY) if module else ({}, {})
    right = wrong = empty = 0
    for name, answer in ANSWERS.items():
        if not answer.strip():
            print(f"{name}: ответ не вписан")
            empty += 1
            continue
        parts = [normalize_big_o(p) for p in answer.split("/")]
        expected = key.get(name)
        ok = expected is not None and len(parts) == 2 and all(
            part in {normalize_big_o(v) for v in variants} for part, variants in zip(parts, expected)
        )
        right += ok
        wrong += not ok
        shown = " / ".join(variants[0] for variants in expected) if expected else "?"
        print(f"{name}: {'✅' if ok else '❌'}  твой: {answer.strip()}   верно: {shown}")
        if name in why:
            print("    почему:", why[name])
    print(f"\nИтого: верно {right}, ошибок {wrong}, не отвечено {empty}")

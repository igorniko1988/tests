"""Проверка упражнений «что выведет» (drills.py в папке каждого раздела).

Вызывается из drills.py раздела, отдельно не запускается.
Запускает каждый фрагмент, сравнивает вывод с ответом и показывает объяснение
из <урок>/solutions/drills_explain.py. Пока ответ пустой, правильный вывод не показывается.
"""

import contextlib
import importlib.util
import io
from pathlib import Path


def actual_output(code: str) -> str:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {"__name__": "__drill__"})
    except Exception as e:  # noqa: BLE001
        return " | ".join([*buf.getvalue().splitlines(), type(e).__name__])
    return " | ".join(buf.getvalue().splitlines())


def normalize(text: str) -> str:
    return " | ".join(part.strip() for part in text.strip().split("|"))


def load_explain(drills_file: str) -> dict[str, str]:
    path = Path(drills_file).resolve().parents[1] / "solutions" / "drills_explain.py"
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("drills_explain", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.EXPLAIN


def run(D: dict[str, str], A: dict[str, str], drills_file: str) -> None:
    explain = load_explain(drills_file)
    right = wrong = empty = 0
    for key, code in D.items():
        print(f"── {key} " + "─" * 50, code.rstrip(), sep="")
        mine = A.get(key, "").strip()
        if not mine:
            print(f"   ответ не вписан — заполни A[{key!r}]\n")
            empty += 1
            continue
        real = actual_output(code)
        ok = normalize(mine) == normalize(real)
        right += ok
        wrong += not ok
        print(f"   твой ответ: {mine}")
        print(f"   на деле:    {real}")
        print("   ✅ верно" if ok else "   ❌ ошибка")
        if key in explain:
            print("   почему:", explain[key])
        print()
    print(f"Итого: верно {right}, ошибок {wrong}, не отвечено {empty}")

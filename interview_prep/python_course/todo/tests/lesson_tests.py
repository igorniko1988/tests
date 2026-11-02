"""Берёт тесты урока и оставляет только те, чьи задачи лежат в todo/<модуль>."""
import importlib.util
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]


def collect(lesson_test: str, module: str) -> dict:
    spec = importlib.util.spec_from_file_location(f"lesson_{module}", COURSE / lesson_test)
    lesson = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lesson)
    tasks = {p.stem.split("_")[0] for p in (COURSE / "todo" / module).glob("t[0-9]*.py")}
    return {
        name: obj
        for name, obj in vars(lesson).items()
        if name.startswith("test_") and name.split("_")[1] in tasks
    }

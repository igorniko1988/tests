"""Тесты задач из week2_core — те же, что в уроках, но грузят файлы этой папки.

Имя теста = <модуль>_<тест урока>, поэтому `uv run pytest -k c04_t01` гоняет одну задачу.
"""
import importlib.util
import os
import sys
from pathlib import Path

import pytest

CORE = Path(__file__).resolve().parents[1]
COURSE = CORE.parent
# SRC=solutions — прогнать тесты на эталоне урока; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")

LESSONS = {
    "c04": "week2/c04_functions",
    "c05": "week2/c05_generators",
    "c06": "week2/c06_decorators",
    "a03": "week2/a03_two_pointers",
    "a04": "week2/a04_sliding_window",
    "a05": "week2/a05_stack_queue",
    "q2": "week2/q2_function_utils",
}


def load_file(path: Path, name: str):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def make_load(prefix: str, lesson_dir: Path):
    def load(name):
        if SRC != "tasks":
            return load_file(lesson_dir / "solutions" / f"{name}.py", f"core_solution_{prefix}_{name}")
        path = CORE / f"{prefix}_{name}.py"
        if not path.exists():
            pytest.skip(f"{name} нет в week2_core (доп. задача урока)")
        return load_file(path, f"core_{prefix}_{name}")

    return load


def collect(prefix: str) -> dict:
    lesson_dir = COURSE / LESSONS[prefix]
    test_file = next((lesson_dir / "tests").glob("test_*.py"))
    lesson = load_file(test_file, f"core_lesson_{prefix}")
    lesson.load = make_load(prefix, lesson_dir)
    tasks = {p.stem.split("_")[1] for p in CORE.glob(f"{prefix}_t[0-9]*.py")}
    return {
        f"test_{prefix}_{name[5:]}": obj
        for name, obj in vars(lesson).items()
        if name.startswith("test_") and name.split("_")[1] in tasks
    }


for _prefix in LESSONS:
    globals().update(collect(_prefix))

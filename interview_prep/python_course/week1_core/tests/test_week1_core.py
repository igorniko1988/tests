"""Тесты задач из week1_core — те же, что в уроках недели 1, но грузят файлы этой папки.

Имя теста = <модуль>_<тест урока>, поэтому `uv run pytest -k a2_t01` гоняет только two_sum.
"""
import importlib.util
import os
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
COURSE = CORE.parent
# SRC=solutions — прогнать тесты на эталоне урока; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")

LESSONS = {
    "a1": "week1/a1_arrays_strings",
    "a2": "week1/a2_hashing",
    "q1": "week1/q1_data",
    "x1": "week1/x1_exam",
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
        if SRC == "tasks":
            return load_file(CORE / f"{prefix}_{name}.py", f"core_{prefix}_{name}")
        return load_file(lesson_dir / "solutions" / f"{name}.py", f"core_solution_{prefix}_{name}")

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

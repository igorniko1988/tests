"""Собирает все уроки UI-части в один документ practice/UI_COURSE.md.

Запуск:  uv run python practice/build_ui_course.py

Для каждого урока берёт теорию (practice/uN_MM_*.md), условия задач (docstring из practice/tasks/) и файл для ревью, если он есть. Заголовки теории сдвигаются на уровень ниже,
блоки кода не трогаются. Документ пересобирается целиком — руками его не правят.
"""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRACTICE = ROOT / "practice"
TASKS = PRACTICE / "tasks"
OUT = PRACTICE / "UI_COURSE.md"

MODULES = {
    1: "Основы и устройство Playwright",
    2: "Ожидания и устойчивые тесты",
    3: "Сложные элементы и сценарии",
    4: "Page Object и архитектура",
    5: "Данные, авторизация и API внутри Playwright",
    6: "Сеть и окружение браузера",
    7: "Отладка и отчёты",
    8: "Качество: визуал, доступность, производительность",
    9: "Масштаб и CI",
    10: "Senior и собеседования",
}


def lesson_key(path: Path) -> tuple[int, int]:
    module, lesson = re.match(r"u(\d+)_(\d+)_", path.name).groups()
    return int(module), int(lesson)


def shift_headings(markdown: str, levels: int) -> str:
    """Сдвинуть заголовки вне блоков кода: '## x' → '#### x' при levels=2."""
    out, in_code = [], False
    for line in markdown.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"#{1,6} ", line):
            line = "#" * levels + line
        out.append(line)
    return "\n".join(out)


def tasks_of(path: Path) -> str | None:
    """Docstring модуля — условия задач (код решений в документ не попадает)."""
    if not path.exists():
        return None
    return ast.get_docstring(ast.parse(path.read_text(encoding="utf-8")))


def task_file(module: int, lesson: int) -> Path | None:
    for folder in (TASKS, PRACTICE):
        for path in sorted(folder.glob(f"*u{module}_{lesson:02d}_*.py")):
            if "review_me" not in path.name and "build_" not in path.name:
                return path
    return None


def main() -> None:
    theories = sorted(PRACTICE.glob("u*_*_*.md"), key=lesson_key)
    lessons = []
    for theory in theories:
        module, lesson = lesson_key(theory)
        text = theory.read_text(encoding="utf-8")
        title_line, _, body = text.partition("\n")
        title = re.sub(r"^#\s*U\d+\.\s*Урок\s*\d+\s*[—-]\s*", "", title_line).strip()
        title = title[:1].upper() + title[1:]
        lessons.append((module, lesson, title, theory, body))

    parts = [
        "# Курс «UI-автоматизация на Playwright + Python», все уроки\n",
        "Собрано скриптом `practice/build_ui_course.py` из файлов уроков — **не править руками**, "
        "править уроки и пересобирать.\n",
        "Каждый урок: теория → задания (условия; решения пишутся в файле заданий) → файл для ревью, если есть.\n",
        "Стенд: `docker compose up -d --build` → http://localhost:8080/app/ (кабинет), "
        "http://localhost:8080/app/lab.html (лаборатория).\n",
        "## Оглавление\n",
    ]
    for module, name in MODULES.items():
        items = [item for item in lessons if item[0] == module]
        if not items:
            continue
        parts.append(f"- **U{module}. {name}**")
        for _, lesson, title, _, _ in items:
            parts.append(f"  - [U{module}.{lesson} {title}](#u{module}-{lesson})")
    parts.append("")

    current_module = None
    for module, lesson, title, theory, body in lessons:
        if module != current_module:
            current_module = module
            parts.append(f"\n---\n\n# U{module}. {MODULES[module]}\n")
        parts.append(f'<a id="u{module}-{lesson}"></a>\n')
        parts.append(f"## U{module}.{lesson} {title}\n")
        parts.append(f"*Теория: `practice/{theory.name}`*\n")
        parts.append(shift_headings(body.strip(), 2))
        tasks_path = task_file(module, lesson)
        tasks = tasks_of(tasks_path) if tasks_path else None
        if tasks:
            parts.append(f"\n### Задания — `{tasks_path.relative_to(ROOT)}`\n")
            parts.append("```text\n" + tasks.strip() + "\n```")
        for review in sorted(PRACTICE.glob(f"u{module}_{lesson:02d}_review_me.py")):
            parts.append(f"\n### Файл для ревью — `practice/{review.name}`\n")
            parts.append("```python\n" + review.read_text(encoding="utf-8").strip() + "\n```")
        parts.append("")

    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: уроков {len(lessons)}, строк {len(OUT.read_text().splitlines())}")


if __name__ == "__main__":
    main()

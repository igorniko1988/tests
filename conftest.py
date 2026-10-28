from pathlib import Path

import pytest

# Плагины подключаются только в корневом conftest: pytest не разрешает pytest_plugins во вложенных.
# Порядок важен: фикстура credentials есть в обоих фреймворках, действует последняя (UI, uuid).
pytest_plugins = [
    "framework.fixtures.api",
    "framework.fixtures.data",
    "ui_framework.fixtures.app",
    "ui_framework.fixtures.data",
    "ui_framework.plugins.reporting",
]

TESTS_DIR = Path(__file__).parent / "tests"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # Маркер слоя по папке: tests/api → api, tests/ui → ui, tests/unit → unit. Запуск: pytest -m api
    for item in items:
        path = Path(item.path)
        if path.is_relative_to(TESTS_DIR):
            layer = path.relative_to(TESTS_DIR).parts[0]
            if layer in ("api", "ui", "unit"):
                item.add_marker(layer)

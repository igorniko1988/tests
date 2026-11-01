"""Маркер слоя по папке: tests/api → api, tests/ui → ui, tests/e2e → e2e, tests/unit → unit.

Тесту не нужно писать @pytest.mark.api руками. Запуск слоя: pytest -m api.
"""

from pathlib import Path

import pytest

LAYERS = ("unit", "api", "ui", "e2e")
TESTS_DIR = Path(__file__).resolve().parents[2] / "tests"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        path = Path(item.path)
        if path.is_relative_to(TESTS_DIR):
            layer = path.relative_to(TESTS_DIR).parts[0]
            if layer in LAYERS:
                item.add_marker(layer)

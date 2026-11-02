# Плагины фреймворка подключаются только здесь: pytest не разрешает pytest_plugins во вложенных conftest.
# Порядок: сначала общее (настройки, данные), потом слои, потом плагины отчётов.
pytest_plugins = [
    "framework.fixtures.config",
    "framework.fixtures.data",
    "framework.fixtures.api",
    "framework.fixtures.ui",
    "framework.plugins.markers",
    "framework.plugins.reporting",
]

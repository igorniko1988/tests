"""Отчёты: шапка прогона, окружение в Allure, артефакты браузера при падении."""

from pathlib import Path

import allure
import pytest
from playwright.sync_api import expect

from framework.config.settings import get_settings


def pytest_configure(config: pytest.Config) -> None:
    # Таймаут expect(...) для всех UI-проверок
    expect.set_options(timeout=get_settings().expect_timeout_ms)


def pytest_report_header(config: pytest.Config) -> str:
    settings = get_settings()
    return f"env {settings.env}, base_url {settings.base_url}"


def pytest_sessionstart(session: pytest.Session) -> None:
    results_dir = session.config.getoption("--alluredir", default=None)
    if results_dir:
        settings = get_settings()
        Path(results_dir).mkdir(parents=True, exist_ok=True)
        (Path(results_dir) / "environment.properties").write_text(
            f"env={settings.env}\nbase_url={settings.base_url}\n"
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(page.url, name="url", attachment_type=allure.attachment_type.TEXT)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item: pytest.Item):
    yield
    # Playwright сохраняет скриншоты, видео и trace в teardown своих фикстур — к этому моменту они уже на диске
    output_path = item.funcargs.get("output_path")
    if not output_path or not Path(output_path).exists():
        return
    for file in Path(output_path).iterdir():
        if file.suffix == ".png":
            allure.attach.file(str(file), name=file.name, attachment_type=allure.attachment_type.PNG)
        elif file.suffix == ".webm":
            allure.attach.file(str(file), name=file.name, attachment_type=allure.attachment_type.WEBM)
        elif file.suffix == ".zip":
            allure.attach.file(str(file), name=file.name, extension="zip")

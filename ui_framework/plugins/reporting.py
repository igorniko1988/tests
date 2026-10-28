from pathlib import Path

import allure
import pytest

from ui_framework.config.settings import Settings


def pytest_sessionstart(session):
    results_dir = session.config.getoption('--alluredir', default=None)
    if results_dir:
        settings = Settings()
        Path(results_dir).mkdir(parents=True, exist_ok=True)
        (Path(results_dir) / 'environment.properties').write_text(
            f'env={settings.env}\nbase_url={settings.base_url}\n'
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(page.url, name="url", attachment_type=allure.attachment_type.TEXT)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
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

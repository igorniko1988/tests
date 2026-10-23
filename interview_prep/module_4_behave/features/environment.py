import functools
import http.server
import pathlib
import threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
SCREENSHOTS = ROOT / "screenshots"


def before_all(context):
    """Один раз на весь прогон: локальный сервер со страницами."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE_DIR))
    handler.log_message = lambda *args, **kwargs: None
    context.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=context.server.serve_forever, daemon=True).start()
    context.base_url = f"http://127.0.0.1:{context.server.server_address[1]}"
    # параметры из командной строки: behave -D browser=firefox -D headed=1
    userdata = context.config.userdata
    context.browser = userdata.get("browser", "chrome")
    context.headed = userdata.get("headed", "0") == "1"


def before_scenario(context, scenario):
    """Перед каждым сценарием: браузер только для сценариев с тегом @ui."""
    if "ui" in scenario.effective_tags:
        from selenium import webdriver

        if context.browser == "firefox":
            options = webdriver.FirefoxOptions()
            if not context.headed:
                options.add_argument("-headless")
            context.driver = webdriver.Firefox(options=options)
        else:
            options = webdriver.ChromeOptions()
            if not context.headed:
                options.add_argument("--headless=new")
            options.add_argument("--window-size=1280,900")
            context.driver = webdriver.Chrome(options=options)


def after_step(context, step):
    """После каждого шага: скриншот, если шаг упал."""
    if step.status == "failed" and hasattr(context, "driver"):
        SCREENSHOTS.mkdir(exist_ok=True)
        name = f"{step.name[:40]}".replace(" ", "_").replace('"', "")
        context.driver.save_screenshot(str(SCREENSHOTS / f"{name}.png"))


def after_scenario(context, scenario):
    """После каждого сценария: закрыть браузер, даже если сценарий упал."""
    if hasattr(context, "driver"):
        context.driver.quit()
        del context.driver


def after_all(context):
    context.server.shutdown()

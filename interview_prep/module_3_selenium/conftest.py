import functools
import http.server
import pathlib
import threading

from selenium import webdriver
import pytest
from selenium import webdriver

SITE_DIR = pathlib.Path(__file__).parent / "site"




def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="show the browser window")
    parser.addoption("--browser", default="chrome", choices=["chrome", "firefox"])


@pytest.fixture(scope="session")
def base_url():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE_DIR))
    handler.log_message = lambda *args, **kwargs: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


@pytest.fixture
def driver(request):
    headed = request.config.getoption("--headed")
    browser = request.config.getoption("--browser")
    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if not headed:
            options.add_argument("-headless")
        drv = webdriver.Firefox(options=options)
    else:
        options = webdriver.ChromeOptions()
        if not headed:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,900")
        drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

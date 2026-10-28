import inspect

import pytest

from tasks import task_01_open_page as t1
from tasks import task_02_locators as t2
from tasks import task_03_login as t3
from tasks import task_04_wait as t4
from tasks import task_05_form as t5


def test_task_01_title(driver, base_url):
    assert t1.get_title(driver, base_url) == "Login Page"


@pytest.fixture
def login_page(driver, base_url):
    driver.get(f"{base_url}/login.html")
    return driver


def test_task_02_by_id(login_page):
    el = t2.find_username_by_id(login_page)
    assert el.tag_name == "input"
    assert el.get_attribute("id") == "username"


def test_task_02_by_css(login_page):
    el = t2.find_login_button_by_css(login_page)
    assert el.tag_name == "button"
    assert el.get_attribute("id") == "login-btn"


def test_task_02_by_xpath(login_page):
    el = t2.find_help_link_by_xpath(login_page)
    assert el.tag_name == "a"
    assert el.text == "Help"


def test_task_02_by_testid(login_page):
    el = t2.find_password_by_testid(login_page)
    assert el.get_attribute("id") == "password"


@pytest.mark.parametrize("user,password,message", [
    ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"),
    ("tomsmith", "wrong", "Your username or password is invalid!"),
    ("nobody", "SuperSecretPassword!", "Your username or password is invalid!"),
], ids=["valid", "bad-password", "bad-user"])
def test_task_03_login(driver, base_url, user, password, message):
    assert t3.login(driver, base_url, user, password) == message


def test_task_04_wait(driver, base_url):
    assert t4.get_dynamic_text(driver, base_url) == "Hello World!"


def test_task_04_no_sleep():
    assert "sleep(" not in inspect.getsource(t4.get_dynamic_text)


def test_task_05_select(driver, base_url):
    assert t5.select_country(driver, base_url, "Poland") == "Poland"


def test_task_05_checkbox(driver, base_url):
    assert t5.tick_agree(driver, base_url) is True


def test_task_05_items(driver, base_url):
    assert t5.get_items(driver, base_url) == ["Apple", "Banana", "Cherry"]


def test_task_05_table(driver, base_url):
    assert t5.get_admin_name(driver, base_url) == "Anna"

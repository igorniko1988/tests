import importlib
import os

import pytest

# SRC=solutions — прогнать тесты на эталоне; по умолчанию — твои решения в этой папке.
SRC = os.environ.get("SRC", "tasks")


def load(name):
    return importlib.import_module(name if SRC == "tasks" else f"{SRC}.{name}")


class FakeSession:
    def __init__(self, status=200):
        self.calls = []
        self.status = status

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return {"status": self.status}


class FakeBrowser:
    def __init__(self, visible=True, rows=()):
        self.actions = []
        self.visible = visible
        self._rows = list(rows)

    def goto(self, path):
        self.actions.append(("goto", path))

    def is_visible(self, selector):
        self.actions.append(("is_visible", selector))
        return self.visible

    def fill(self, selector, value):
        self.actions.append(("fill", selector, value))

    def click(self, selector):
        self.actions.append(("click", selector))

    def select(self, selector, value):
        self.actions.append(("select", selector, value))

    def text(self, selector):
        return "Ann"

    def texts(self, selector):
        return list(self._rows)


# ---------- t01 ----------
def test_t01_base_client():
    session = FakeSession()
    client = load("t01_client_hierarchy").BaseClient("http://api", session)
    assert client.request("GET", "/health", timeout=1) == {"status": 200}
    assert session.calls == [("GET", "http://api/health", {"headers": {"Accept": "application/json"}, "timeout": 1})]


def test_t01_users_client():
    module = load("t01_client_hierarchy")
    session = FakeSession()
    users = module.UsersClient("http://api", session, token="t1")
    assert isinstance(users, module.BaseClient)
    users.get_user(7)
    users.create_user(name="ann")
    headers = {"Accept": "application/json", "Authorization": "Bearer t1"}
    assert session.calls == [
        ("GET", "http://api/users/7", {"headers": headers}),
        ("POST", "http://api/users", {"headers": headers, "json": {"name": "ann"}}),
    ]
    assert users.base_url == "http://api"


# ---------- t02 ----------
def test_t02_mro_prediction():
    module = load("t02_predict_mro")
    assert module.ANSWER_MRO == [k.__name__ for k in module.Final.__mro__], "порядок MRO предсказан неверно"


def test_t02_calls_prediction():
    module = load("t02_predict_mro")
    assert module.ANSWER_CALLS == module.Final().setup(), "порядок вызовов super() предсказан неверно"


# ---------- t03 ----------
def test_t03_abstract_base():
    module = load("t03_abstract_page")
    with pytest.raises(TypeError):
        module.BasePage(FakeBrowser())

    class NoLoaded(module.BasePage):
        path = "/x"

    with pytest.raises(TypeError):
        NoLoaded(FakeBrowser())


def test_t03_login_page():
    module = load("t03_abstract_page")
    browser = FakeBrowser()
    page = module.LoginPage(browser).open()
    assert isinstance(page, module.LoginPage)
    page.login("a@b.io", "secret")
    assert browser.actions == [
        ("goto", "/app/login.html"),
        ("is_visible", "[data-testid=login-form]"),
        ("fill", "[data-testid=email]", "a@b.io"),
        ("fill", "[data-testid=password]", "secret"),
        ("click", "[data-testid=submit]"),
    ]


def test_t03_not_loaded():
    with pytest.raises(AssertionError, match="LoginPage is not loaded"):
        load("t03_abstract_page").LoginPage(FakeBrowser(visible=False)).open()


# ---------- t04 ----------
def test_t04_dashboard_composition():
    module = load("t04_composition")
    browser = FakeBrowser(rows=["o1", "o2"])
    page = module.DashboardPage(browser)
    assert page.place_and_count("BUY", 3) == 2
    assert browser.actions == [
        ("select", "[data-testid=side]", "BUY"),
        ("fill", "[data-testid=qty]", "3"),
        ("click", "[data-testid=place]"),
    ]
    page.header.logout()
    assert browser.actions[-1] == ("click", "[data-testid=logout]")
    assert page.header.user_name() == "Ann"
    assert page.orders_table.rows() == ["o1", "o2"]


def test_t04_no_inheritance():
    module = load("t04_composition")
    for component in (module.Header, module.OrderForm, module.OrdersTable):
        assert not issubclass(module.DashboardPage, component)
    page = module.DashboardPage(FakeBrowser())
    assert isinstance(page.order_form, module.OrderForm) and isinstance(page.orders_table, module.OrdersTable)


# ---------- t05 ----------
def make_service(module, session):
    return module.OrderService(module.OrderValidator(), module.OrdersApi(session), module.ReportFormatter())


def test_t05_validator():
    v = load("t05_refactor_srp").OrderValidator()
    assert v.validate({"symbol": "BTC", "qty": 1, "side": "BUY"}) == []
    assert v.validate({}) == ["symbol is required", "qty must be positive", "side must be BUY or SELL"]
    assert v.validate({"symbol": "BTC", "qty": 0, "side": "BUY"}) == ["qty must be positive"]


def test_t05_service_places_order():
    module = load("t05_refactor_srp")
    session = FakeSession()
    order = {"symbol": "BTC", "qty": 2, "side": "SELL"}
    assert make_service(module, session).place(order) == "SELL 2 BTC: 200"
    assert session.calls == [("POST", "/orders", {"json": order})]


def test_t05_service_rejects_invalid():
    module = load("t05_refactor_srp")
    session = FakeSession()
    with pytest.raises(ValueError, match="symbol is required; side must be BUY or SELL"):
        make_service(module, session).place({"qty": 1, "side": "HOLD"})
    assert session.calls == []


def test_t05_parts_are_independent():
    module = load("t05_refactor_srp")
    assert module.ReportFormatter().format({"side": "BUY", "qty": 1, "symbol": "ETH"}, {"status": 201}) == "BUY 1 ETH: 201"
    session = FakeSession()
    module.OrdersApi(session).create({"a": 1})
    assert session.calls == [("POST", "/orders", {"json": {"a": 1}})]


# ---------- t06 ★ ----------
def test_t06_logging_mixin():
    module = load("t06_logging_mixin")
    session = FakeSession(status=204)
    users = module.LoggedUsersClient(session)
    orders = module.LoggedOrdersClient(session)
    users.get_user(1)
    orders.cancel(9)
    orders.cancel(10)
    assert users.request_log == ["GET /users/1", "-> 204"]
    assert orders.request_log == ["DELETE /orders/9", "-> 204", "DELETE /orders/10", "-> 204"]
    assert session.calls == [("GET", "/users/1", {}), ("DELETE", "/orders/9", {}), ("DELETE", "/orders/10", {})]
    assert module.LoggedUsersClient.__mro__[1] is module.LoggingMixin
    assert "__init__" not in vars(module.LoggingMixin)

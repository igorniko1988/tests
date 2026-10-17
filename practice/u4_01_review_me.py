"""U4.1, задача 6 — ревью Page Object от «коллеги».

Код рабочий (почти), но на ревью его не пропустят. Найди минимум 10 проблем.
Для каждой: строка, что не так, как исправить. Ответы — внизу файла.
Подсказка: сверяйся с разделом 7 теории (антипаттерны) и с U2.1–U2.2.
"""

import time

from playwright.sync_api import Page, expect

EMAIL = "trader@test.com"
PASSWORD = "password123"


class ExchangePage:
    LOGIN_BUTTON = "[data-testid=login-button]"
    REGISTER_BUTTON = "text=Зарегистрироваться"
    DEPOSIT_BUTTON = "#deposit-form > button"

    def __init__(self, page: Page):
        self.page = page
        self.last_order_price = None

    def open(self):
        self.page.goto("http://localhost:8080/app/")
        self.page.wait_for_load_state("networkidle")

    def click_register_button(self):
        self.page.click(self.REGISTER_BUTTON)

    def login(self):
        self.page.fill("[data-testid=email-input]", EMAIL)
        self.page.fill("[data-testid=password-input]", PASSWORD)
        self.page.click(self.LOGIN_BUTTON)
        time.sleep(2)

    def deposit_and_check(self, asset, amount):
        self.page.select_option("[data-testid=deposit-asset]", asset)
        self.page.fill("[data-testid=deposit-amount]", amount)
        self.page.click(self.DEPOSIT_BUTTON)
        expect(self.page.locator(f"[data-asset={asset}] [data-testid=balance-available]")).to_have_text(amount)

    def get_balance(self, asset):
        return self.page.locator(f"[data-asset={asset}] [data-testid=balance-available]").text_content()

    def place_order(self, price, quantity):
        self.page.fill("[data-testid=order-price]", price)
        self.page.fill("[data-testid=order-quantity]", quantity)
        self.page.click("[data-testid=place-order-button]")
        self.last_order_price = price

    def cancel_last_order(self):
        self.page.locator("[data-testid=cancel-order]").first.click()

    def is_order_cancelled(self):
        return "CANCELED" in self.page.locator("[data-testid=order-status]").first.text_content()

    def logout(self):
        try:
            self.page.click("[data-testid=logout-button]", timeout=1000)
        except Exception:
            pass


def test_order_flow(page: Page):
    exchange = ExchangePage(page)
    exchange.open()
    exchange.login()
    exchange.deposit_and_check("USDT", "1000")
    exchange.place_order("100", "1")
    assert exchange.get_balance("USDT") == "900"
    exchange.cancel_last_order()
    assert exchange.is_order_cancelled()


# Ответы
"""
1. стр. 17, class ExchangePage — God object: вход, пополнение, ордера в одном классе на всё
   приложение. Разбить по экранам: AuthPage, DashboardPage (+ компоненты в U4.2).
2. стр. 18–20 — селекторы строками-константами и page.click(...): теряем get_by_role, strict mode,
   цепочки. Локаторы — атрибутами Locator в __init__.
3. стр. 19 — "text=Зарегистрироваться": поиск по подстроке текста, хрупкий и не по роли.
   get_by_role("button", name="Зарегистрироваться").
4. стр. 20 — "#deposit-form > button": завязка на вложенность DOM. Внутри формы get_by_role.
5. стр. 13–14, 31–32 — тестовые данные (EMAIL, PASSWORD) зашиты в PO, login() без аргументов —
   PO знает про конкретный тест, войти другим пользователем нельзя. login(email, password).
6. стр. 24, 51 — состояние в PO (self.last_order_price): неявная связь шагов, никем не читается.
   Убрать; нужное следующим шагам — возвращать из метода (id ордера из ответа).
7. стр. 27 — абсолютный URL в goto: не переключить окружение. Относительный путь + base_url.
8. стр. 28 — wait_for_load_state("networkidle"): у нас SPA с опросом ордеров раз в 2 с — может
   не наступить, и это не признак готовности. Ждать конкретный элемент экрана (wait_loaded).
   open() ничего не возвращает — не построить цепочку; вернуть self.
9. стр. 30 — метод на клик click_register_button(): смысла не добавляет. register(email, password)
   -> DashboardPage.
10. стр. 31–32 — data-testid=email-input/password-input существуют, но get_by_label("Email")
    проверяет ещё и доступность формы. (Не баг, но приоритет локаторов.)
11. стр. 36 — time.sleep(2): медленно и всё равно флейк. Ждать кабинет: expect(root).to_be_visible(),
    login() возвращает DashboardPage.
12. стр. 38–42 — deposit_and_check: метод на тест + бизнес-проверка внутри PO. Негативный тест
    пополнения с ним не написать. Разделить: deposit() (ждёт 2xx ответа) и проверка в тесте.
    Ещё: to_have_text(amount) — баланс мог быть ненулевым до пополнения, ожидание неверное.
13. стр. 42, 45 — f"[data-asset={asset}] ..." дублируется — вынести balance_available(asset)
    -> Locator; селектор без привязки к balance-row может совпасть с чем-то ещё.
14. стр. 44–45 — get_balance() -> str через text_content(): проверка «в моменте», стр. 72
    assert == "900" — флейк (балансы перезагружаются асинхронно). Вернуть Locator, в тесте expect.
15. стр. 47–51 — place_order не выбирает пару и сторону (надеется на значения по умолчанию),
    не ждёт ответа сервера и не возвращает id созданного ордера.
16. стр. 53–54 — cancel_last_order: .first — «первый попавшийся», а не нужный ордер. Порядок строк —
    деталь реализации. cancel_order(order_id) по data-id строки.
17. стр. 56–57 — is_order_cancelled() -> bool: проверка в моменте (U2.1) и снова .first.
    order_status(order_id) -> Locator, в тесте expect(...).to_have_text("CANCELED").
18. стр. 59–63 — try/except Exception: pass глушит любую ошибку, timeout=1000 — магическое число.
    Если выйти не удалось, тест должен упасть. logout() -> AuthPage с wait_loaded.
19. стр. 66–74 — тест: пользователь trader@test.com общий для всех прогонов — после первого прогона
    баланс уже не 1000, параллельный запуск ломается; нет регистрации уникального пользователя
    и teardown (открытые ордера в общем стакане).
20. Нет аннотаций типов у аргументов и возвращаемых значений — IDE не подскажет, что вернёт метод.
"""

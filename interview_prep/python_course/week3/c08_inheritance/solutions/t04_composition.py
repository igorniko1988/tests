class Header:
    def __init__(self, browser) -> None:
        self.browser = browser

    def logout(self) -> None:
        self.browser.click("[data-testid=logout]")

    def user_name(self) -> str:
        return self.browser.text("[data-testid=user-name]")


class OrderForm:
    def __init__(self, browser) -> None:
        self.browser = browser

    def place(self, side: str, qty: int) -> None:
        self.browser.select("[data-testid=side]", side)
        self.browser.fill("[data-testid=qty]", str(qty))
        self.browser.click("[data-testid=place]")


class OrdersTable:
    def __init__(self, browser) -> None:
        self.browser = browser

    def rows(self) -> list[str]:
        return self.browser.texts("[data-testid=order-row]")

    def count(self) -> int:
        return len(self.rows())


class DashboardPage:
    def __init__(self, browser) -> None:
        self.header = Header(browser)
        self.order_form = OrderForm(browser)
        self.orders_table = OrdersTable(browser)

    def place_and_count(self, side: str, qty: int) -> int:
        self.order_form.place(side, qty)
        return self.orders_table.count()

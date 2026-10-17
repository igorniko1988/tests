from playwright.sync_api import Page, expect
from ui_framework.pages.base_page import BasePage
from ui_framework.components.common import Header
from ui_framework.components.forms import DepositForm, OrderForm
from ui_framework.components.tables import BalancesTable, OrdersTable


class DashboardPage(BasePage):
    path = '/app/'

    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard = self.page.get_by_test_id('dashboard')
        self.header = Header(page)
        self.balances = BalancesTable(page)
        self.deposit_form = DepositForm(page)
        self.order_form = OrderForm(page)
        self.orders = OrdersTable(page)

    def wait_loaded(self):
        expect(self.dashboard).to_be_visible()
        return self

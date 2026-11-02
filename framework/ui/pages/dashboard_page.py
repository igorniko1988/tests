import allure
from playwright.sync_api import Page, expect

from framework.ui.components.common import Header
from framework.ui.components.forms import DepositForm, OrderForm
from framework.ui.components.tables import BalancesTable, OrdersTable
from framework.ui.pages.base_page import BasePage


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

    @allure.step('Дождаться личного кабинета')
    def wait_loaded(self):
        expect(self.dashboard).to_be_visible()
        return self

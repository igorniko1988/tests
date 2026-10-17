from playwright.sync_api import Locator, Page


class Table:
    """Любая <table>: колонка по тексту заголовка. Получает локатор самой таблицы."""

    def __init__(self, table: Locator):
        self.table = table
        self.header_cells = table.locator('thead th')
        self.body_rows = table.locator('tbody tr')

    def column_index(self, name):
        # Заголовки статичны и есть в HTML сразу, поэтому all_text_contents() без ожидания здесь безопасен
        return self.header_cells.all_text_contents().index(name) + 1

    def column(self, name):
        return self.table.locator(f'tbody td:nth-child({self.column_index(name)})')


class BalancesTable:
    def __init__(self, page: Page):
        self.page = page
        self.table = Table(page.get_by_test_id('balances-table'))
        self.rows = page.get_by_test_id('balance-row')

    def row(self, asset):
        return self.rows.and_(self.page.locator(f'[data-asset="{asset}"]'))

    def available(self, asset):
        return self.row(asset).get_by_test_id('balance-available')

    def locked(self, asset):
        return self.row(asset).get_by_test_id('balance-locked')


class OrderRow:
    """Одна строка ордера. Получает локатор своей строки и таблицу — чтобы искать ячейку по имени колонки."""

    def __init__(self, row: Locator, table: Table):
        self.row = row
        self.table = table
        self.page = row.page
        self.status = row.get_by_test_id('order-status')
        self.filled = row.get_by_test_id('order-filled')
        self.cancel_button = row.get_by_role('button', name='Отменить')

    def cell(self, column_name):
        return self.row.locator(f'td:nth-child({self.table.column_index(column_name)})')

    def cancel(self):
        with self.page.expect_response(lambda r: r.request.method == 'DELETE' and '/orders/' in r.url) as info:
            self.cancel_button.click()
        return info.value


class OrdersTable:
    def __init__(self, page: Page):
        self.page = page
        self.table = Table(page.get_by_test_id('orders-table'))
        self.rows = page.get_by_test_id('order-row')
        self.empty = page.get_by_test_id('orders-empty')
        self.status_filter = page.get_by_test_id('orders-filter')

    def row(self, order_id):
        return OrderRow(self.rows.and_(self.page.locator(f'[data-id="{order_id}"]')), self.table)

    def filter_by_status(self, status):
        """status: "" (все), NEW, PARTIALLY_FILLED, FILLED, CANCELED. Ждёт ответ на запрос с этим фильтром."""
        expected_url = f'/orders?status={status}' if status else '/orders'
        with self.page.expect_response(lambda r: r.request.method == 'GET' and r.url.endswith(expected_url)):
            self.status_filter.select_option(status)

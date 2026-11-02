"""C8 t04 (required, ~20 min). A page built from components.

Build a page by COMPOSITION, not inheritance.

Components (each created with a browser):
- Header: logout() -> browser.click("[data-testid=logout]");
          user_name() -> browser.text("[data-testid=user-name]").
- OrderForm: place(side, qty) -> browser.select("[data-testid=side]", side),
             browser.fill("[data-testid=qty]", str(qty)), browser.click("[data-testid=place]").
- OrdersTable: rows() -> browser.texts("[data-testid=order-row]") (a list of strings);
               count() -> number of rows.

DashboardPage(browser):
- attributes header, order_form, orders_table - component instances sharing the browser;
- place_and_count(side, qty) -> places an order and returns orders_table.count().

Requirements:
- DashboardPage must not inherit from any component (the test checks it).

Follow-up questions:
- Why is "DashboardPage(OrderForm, OrdersTable)" a bad idea?

Run (from interview_prep/python_course/week3/c08_inheritance): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 7.
"""


class Header:
    pass


class OrderForm:
    pass


class OrdersTable:
    pass


class DashboardPage:
    pass

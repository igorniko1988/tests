"""U4. Урок 2 — компоненты.

Теория: practice/u4_02_components.md
Код компонентов — ui_framework/components/ (заготовки base, common, forms, tables), тесты — здесь.
Запуск:
    uv run pytest tests/ui/test_u4_02_components.py tests/ui/test_u4_01_page_object.py -v

Правила:
    - внутри компонента только self.root... (кроме ответов сети и того, что физически вне блока);
    - компоненты не знают о страницах и друг о друге; переходы между экранами возвращает страница;
    - в тестах нет page.get_by_* / page.locator.

Задача 1. BaseComponent (base.py): __init__(root) — self.root и self.page = root.page.

Задача 2. Toast и Header (common.py).
    Toast: wait_hidden(). Header: email (Locator), logout() — только клик.
    В BasePage self.toast теперь — компонент Toast, а не голый Locator.

Задача 3. Формы (forms.py).
    DepositForm: asset, amount, submit_button; deposit(asset, amount) -> dict (ждёт ответ, падает не на 2xx);
                 deposit_expecting_error(asset, amount).
    OrderForm:   symbol, price, quantity, error, submit_button; side(side) — выбрать радио «Купить»/«Продать»;
                 place(side, price, quantity, symbol="ETH-USDT") -> dict; place_expecting_error(...).

Задача 4. Table (tables.py): header_cells, body_rows, column_index(name), column(name) -> Locator.
    BalancesTable(Table): row(asset), available(asset), locked(asset).

Задача 5. OrderRow и OrdersTable (tables.py).
    OrderRow: status, filled, cancel_button; cell(column_name) -> Locator; cancel() -> dict (ждёт DELETE).
        Подумай: откуда OrderRow узнает индекс колонки по имени? (Ему нужна таблица.)
    OrdersTable: root — карточка ордеров (в неё входят фильтр и «Ордеров пока нет»);
        rows, empty, status_filter; table (Table внутри карточки — композиция);
        row(order_id) -> OrderRow; filter_by_status(status) (""/NEW/.../CANCELED).

Задача 6. DashboardPage из компонентов.
    header, balances, deposit_form, order_form, orders; logout() остаётся на странице (переход).
    Реши, оставлять ли фасады deposit()/place_order() из U4.1 (раздел 8 теории). Тесты U4.1 должны
    проходить — либо без изменений (фасад), либо поправь их. Выбор объясни в «Ответах».

Задача 7. Тесты на компоненты.
    а) Ордер с пустой ценой → ошибка формы ордера видна и содержит "price"; строк ордеров 0
       (вспомни U2.1: перед проверкой отсутствия — положительный признак загрузки).
    б) Три BUY (цены 10, 20, 30); отмени 20 через orders.row(id).cancel();
       фильтр CANCELED → одна строка, cell("Цена") == "20"; фильтр NEW → колонка «Цена» == ["30", "10"].
    в) Балансы нового пользователя: колонка «Актив» — все три актива одной проверкой списком
       (сначала посмотри, в каком порядке их отдаёт стенд — порядок в форме пополнения другой);
       доступно 0 у всех трёх (expect.soft).
    г) Выход через dashboard.logout() → AuthPage, форма входа видна; повторный вход тем же email → кабинет.

Задача 8. Структура (письменно в «Ответах»).
    Куда положишь метод «отменить все открытые ордера»: OrdersTable, DashboardPage или хелпер в тесте?
    А «проверить, что ордер исполнился» (ждёт FILLED с таймаутом 15 с)? Почему?

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое компонент в Page Object и зачем он?
    2. Как компонент находит свои элементы?
    3. Наследование или композиция в PO?
    4. Как устроишь работу с таблицей?
    5. Как работаешь с модальными окнами?
    6. Нужны ли фасадные методы на странице?
"""

# Решение пиши в tests/ui/test_u4_02_components.py — файл и папки создаёшь сам.

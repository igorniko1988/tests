# U4. Урок 2 — компоненты

Задания: `tests/ui/test_u4_02_components.py`, код — в `ui_framework/components/`.

План: почему PO страницы разрастается и что такое компонент; корневой локатор и поиск
внутри него; композиция страницы из компонентов; компонент строки таблицы; общий компонент
таблицы и его наследники; тост и шапка как общие компоненты; модальное окно как паттерн;
фасад на странице — нужен ли; антипаттерны; собес.

---

## 1. Зачем компоненты

После U4.1 `DashboardPage` знает всё: шапку, балансы, две формы, таблицу ордеров, тост.
Это уже 15+ методов, и растёт. В реальном приложении хуже:
- та же **таблица** (сортировка, фильтр, пагинация) есть на пяти страницах;
- **шапка** с пользователем и выходом — на всех страницах после входа;
- **тост** / уведомления — глобальные;
- **модалка подтверждения** — одна и та же разметка, разные тексты.

**Компонент** — класс для повторяющейся части экрана. Страница **собирается** из компонентов
(композиция), а не описывает всё сама.

```python
dashboard.deposit_form.deposit("USDT", "1000")
expect(dashboard.balances.available("USDT")).to_have_text("1000")
row = dashboard.orders.row(order_id)
expect(row.status).to_have_text("NEW")
row.cancel()
```

---

## 2. Корневой локатор

Компонент получает **root** — локатор своего блока — и ищет всё **внутри** него:

```python
from playwright.sync_api import Locator


class BaseComponent:
    def __init__(self, root: Locator):
        self.root = root
        self.page = root.page          # если нужен доступ к странице (ответы сети)
```

```python
class DepositForm(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.asset = root.get_by_label("Актив")
        self.amount = root.get_by_placeholder("Сумма")
        self.submit_button = root.get_by_role("button", name="Пополнить")
```

Что это даёт:
- **strict mode решён структурно**: `root.get_by_role("combobox")` в форме пополнения — один элемент,
  хотя на странице их три (U2.2);
- компонент **переиспользуется**: вторая форма пополнения на другой странице — тот же класс с другим root;
- локаторы короче: не нужно в каждом повторять `page.locator("#deposit-form")...`.

Правило: внутри компонента **только `self.root...`**, не `self.page.get_by_...` — иначе компонент
найдёт элементы чужого блока. Исключение — то, что вне DOM-блока: ответы сети (`self.page.expect_response`).

---

## 3. Композиция страницы

```python
class DashboardPage(BasePage):
    path = "/app/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.root = page.get_by_test_id("dashboard")
        self.header = Header(page.get_by_test_id("user-panel"))
        self.balances = BalancesTable(page.get_by_test_id("balances-table"))
        self.deposit_form = DepositForm(page.locator("#deposit-form"))
        self.order_form = OrderForm(page.locator("#order-form"))
        self.orders = OrdersTable(page.get_by_test_id("orders-table").locator(".."))
```

Страница отвечает за **где** (какой root у какого компонента) и за **переходы** между экранами.
Компонент — за **как** внутри своего блока.

У таблицы ордеров root — родитель таблицы (`..`): в него входят и фильтр «Статус», и текст
«Ордеров пока нет». Root выбирай так, чтобы в него попало всё, чем компонент управляет.
Лучше — попросить у разработчиков test-id на контейнер (на стенде у карточки его нет).

---

## 4. Строка таблицы — тоже компонент

```python
class OrderRow(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.status = root.get_by_test_id("order-status")
        self.filled = root.get_by_test_id("order-filled")
        self.cancel_button = root.get_by_role("button", name="Отменить")

    def cancel(self) -> dict:
        with self.page.expect_response(lambda r: r.request.method == "DELETE") as info:
            self.cancel_button.click()
        assert info.value.ok, info.value.text()
        return info.value.json()
```

```python
class OrdersTable(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.rows = root.get_by_test_id("order-row")
        self.empty = root.get_by_test_id("orders-empty")
        self.status_filter = root.get_by_label("Статус")

    def row(self, order_id: str) -> OrderRow:
        return OrderRow(self.rows.and_(self.root.locator(f'[data-id="{order_id}"]')))
```

Тест работает со строкой как с объектом: `orders.row(id).cancel()`, `expect(orders.row(id).status)`.
Локатор строки ленивый — после перерисовки таблицы раз в 2 с объект `OrderRow` продолжает работать
(U2.2: Locator, а не ElementHandle).

---

## 5. Общая таблица и наследники

Логика «колонка по заголовку» (U2.2) одинакова для любой таблицы — её место в базовом классе:

```python
class Table(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.header_cells = root.locator("thead th")
        self.body_rows = root.locator("tbody tr")

    def column_index(self, name: str) -> int:
        return self.header_cells.all_text_contents().index(name) + 1

    def column(self, name: str) -> Locator:
        return self.root.locator(f"tbody td:nth-child({self.column_index(name)})")
```

```python
class BalancesTable(Table):
    def row(self, asset: str) -> Locator:
        return self.root.locator(f'[data-testid="balance-row"][data-asset="{asset}"]')

    def available(self, asset: str) -> Locator:
        return self.row(asset).get_by_test_id("balance-available")
```

`OrdersTable` тоже может наследовать `Table`, но его root — карточка, а не `<table>`.
Тогда `Table` внутри: `self.table = Table(root.locator("table"))` — **композиция вместо наследования**.
Оба варианта нормальны; наследуй, когда «является» (балансы — это таблица), компонуй, когда «содержит»
(карточка ордеров содержит таблицу и фильтр).

Осторожно: `all_text_contents()` не ждёт (U2.1). Заголовки таблицы статичны и есть в HTML сразу,
поэтому здесь можно. Для динамических заголовков — сначала `expect(self.header_cells).not_to_have_count(0)`.

---

## 6. Глобальные компоненты: тост и шапка

```python
class Toast(BaseComponent):
    def wait_hidden(self) -> None:
        expect(self.root).to_be_hidden()
```

Тост один на всё приложение → создаётся в `BasePage`: `self.toast = Toast(page.get_by_test_id("toast"))`.
Шапка есть на всех экранах после входа → в общем предке залогиненных страниц или в каждой такой странице.

Метод `Header.logout()` должен вернуть `AuthPage` — но компонент не должен знать о страницах
(иначе компоненты и страницы импортируют друг друга). Решение: компонент только **кликает**,
переход возвращает страница:

```python
class DashboardPage(BasePage):
    def logout(self) -> "AuthPage":
        self.header.logout()
        return AuthPage(self.page).wait_loaded()
```

---

## 7. Модальное окно (паттерн)

На стенде модалок нет, но на собесе спросят. Типичная модалка подтверждения:

```python
class ConfirmDialog(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.title = root.get_by_role("heading")
        self.confirm_button = root.get_by_role("button", name="Подтвердить")
        self.cancel_button = root.get_by_role("button", name="Отмена")

    def confirm(self) -> None:
        self.confirm_button.click()
        expect(self.root).to_be_hidden()        # синхронизация: окно закрылось
```

```python
class OrderRow(BaseComponent):
    def request_cancel(self) -> ConfirmDialog:
        self.cancel_button.click()
        dialog = ConfirmDialog(self.page.get_by_role("dialog"))
        expect(dialog.root).to_be_visible()
        return dialog
```

Root модалки — `page.get_by_role("dialog")`: окна обычно рендерятся в конец `<body>`, вне блока,
из которого их открыли, поэтому здесь `self.page` оправдан. Метод, открывающий модалку,
**возвращает её компонент** — как переход на другой экран.

Не путать с нативными `alert` / `confirm` браузера — это `page.on("dialog")`, модуль U3.

---

## 8. Фасад на странице — нужен ли

Два стиля:

```python
dashboard.deposit_form.deposit("USDT", "1000")    # через компонент
dashboard.deposit("USDT", "1000")                 # фасад: страница делегирует компоненту
```

| | Только компоненты | Фасад на странице |
|---|---|---|
| Тест | чуть длиннее, видно, с каким блоком работаем | короче |
| Страница | тонкая | дублирует методы компонентов |
| Изменения | правится компонент | компонент + фасад |

Рекомендация: фасадные методы — только для **сценариев**, где участвуют несколько компонентов
или переход («войти», «выйти»). Действия внутри одного блока — через компонент.
В задании 6 ты решишь, оставлять ли `dashboard.deposit()` из U4.1, и объяснишь выбор.

---

## 9. Антипаттерны

| Антипаттерн | Чем плохо |
|---|---|
| `self.page.get_by_...` внутри компонента | находит элементы чужих блоков, strict mode, нельзя переиспользовать |
| компонент знает о страницах (возвращает `AuthPage`) | циклические импорты, компонент нельзя перенести |
| компонент знает о других компонентах | связность; общее — через страницу |
| длинные цепочки в тесте: `dashboard.orders.table.rows.nth(0).cells.nth(2)` | тест снова знает DOM |
| компонент на каждый элемент (`Button`, `Input`) | обёртки без смысла над Locator |
| бизнес-проверки в компонентах | как в PO (U4.1) |
| root, в который не входит часть компонента | фильтр «Статус» вне root таблицы — компонент не может им управлять |

---

## Собес: вопросы и ответы

**1. Что такое компонент в Page Object и зачем он?**
> Класс для повторяющейся части экрана — формы, таблицы, шапки, модалки, тоста. Получает корневой
> локатор и ищет всё внутри него. Страница собирается из компонентов. Это убирает дублирование —
> одна таблица на пяти страницах описана один раз, — уменьшает размер PO страниц и решает
> неоднозначность локаторов: внутри блока элемент уникален.

**2. Как компонент находит свои элементы?**
> Через root: все локаторы строятся от него — `self.root.get_by_role(...)`. На страницу выходит
> только то, что физически вне блока: ответы сети, модалки, которые рендерятся в конец body.

**3. Наследование или композиция в PO?**
> Композиция — по умолчанию: страница содержит компоненты, карточка содержит таблицу и фильтр.
> Наследование — для «является»: таблица балансов — это таблица, она наследует общую логику колонок.
> Наследовать страницы друг от друга не нужно — общее выносится в BasePage или компоненты.

**4. Как устроишь работу с таблицей?**
> Базовый компонент таблицы: заголовки, колонка по имени через индекс, строки. Наследник для
> конкретной таблицы добавляет доменные методы: строку по id, фильтр. Строка — свой компонент
> со статусом и действиями. Тест пишет `orders.row(id).cancel()` и
> `expect(orders.row(id).status).to_have_text(...)`.

**5. Как работаешь с модальными окнами?**
> Модалка — компонент с root `get_by_role("dialog")`. Метод, который её открывает, ждёт видимость
> и возвращает компонент. `confirm()` нажимает кнопку и ждёт, что окно закрылось. Нативные alert
> и confirm браузера — отдельная история, через `page.on("dialog")`.

**6. Нужны ли фасадные методы на странице?**
> Для сценариев, где участвуют несколько компонентов или есть переход, — да: «войти», «выйти».
> Действия внутри одного блока — через компонент, иначе страница дублирует все методы компонентов.

# U4. Урок 5 — Screenplay, собес по модулю U4 и каркас фреймворка

Задания: `practice/tasks/test_u4_05_screenplay_framework.py`, решение — `tests/ui/test_u4_05_screenplay_framework.py` (создаёшь сам), код — `ui_framework/screenplay/`.

План: что такое Screenplay и чем он отличается от Page Object; мини-реализация поверх наших PO;
когда что выбирать; чек-лист готового каркаса UI-фреймворка; шпаргалка и банк вопросов по модулю U4.

---

## 1. Screenplay: идея

Page Object отвечает на вопрос «**что есть на экране** и что с ним можно сделать».
Screenplay — на вопрос «**кто** что делает и **зачем**». Сценарий описывается через участников:

| Понятие | Что это | Пример на стенде |
|---|---|---|
| **Actor** | участник сценария | продавец Алиса, покупатель Боб |
| **Ability** | что актор умеет — обёртка над инструментом | `BrowseTheWeb(page)`, `CallTheApi(client)` |
| **Task** | бизнес-действие из нескольких шагов | `Register`, `Deposit`, `PlaceOrder` |
| **Interaction** | одно низкоуровневое действие | `Click`, `Fill` (часто — методы PO) |
| **Question** | что актор может узнать о системе | `AvailableBalance("USDT")`, `OrderStatus(id)` |

Тест читается как история:

```python
alice = Actor("Алиса").can(BrowseTheWeb(seller_page))
bob = Actor("Боб").can(BrowseTheWeb(buyer_page))

alice.attempts_to(Register(), Deposit("ETH", "1"), PlaceOrder("SELL", price, "1"))
bob.attempts_to(Register(), Deposit("USDT", "1000"), PlaceOrder("BUY", price, "1"))

expect(alice.asks_for(LastOrderStatus())).to_have_text("FILLED", timeout=15_000)
expect(bob.asks_for(AvailableBalance("ETH"))).to_have_text("1")
```

Классическое изложение — Serenity BDD (Java/JS); в Python есть библиотека `screenpy`. На собесе
спрашивают **идею и сравнение с PO**, а не конкретную библиотеку.

---

## 2. Мини-реализация поверх Page Object

Screenplay не заменяет PO целиком: **interactions** и **questions** удобно строить на методах
страниц и компонентов. Минимум кода:

```python
# ui_framework/screenplay/actor.py
from typing import Protocol, TypeVar

T = TypeVar("T")


class Performable(Protocol):
    def perform_as(self, actor: "Actor") -> None: ...


class Answerable(Protocol[T]):
    def answered_by(self, actor: "Actor") -> T: ...


class Actor:
    def __init__(self, name: str):
        self.name = name
        self._abilities: dict[type, object] = {}
        self.memory: dict[str, object] = {}          # что актор запомнил: email, id ордера

    def can(self, *abilities: object) -> "Actor":
        for ability in abilities:
            self._abilities[type(ability)] = ability
        return self

    def ability_to(self, kind: type[T]) -> T:
        try:
            return self._abilities[kind]
        except KeyError:
            raise AssertionError(f"{self.name} не умеет {kind.__name__}") from None

    def attempts_to(self, *tasks: Performable) -> None:
        for task in tasks:
            task.perform_as(self)

    def asks_for(self, question: "Answerable[T]") -> T:
        return question.answered_by(self)
```

```python
# ui_framework/screenplay/abilities.py
class BrowseTheWeb:
    def __init__(self, page: Page):
        self.page = page
        self.app = Application(page)          # способность «пользоваться сайтом» = наш Application (U4.1)
```

```python
# ui_framework/screenplay/tasks.py
class Register:
    def __init__(self, email: str | None = None):
        self.email = email

    def perform_as(self, actor: Actor) -> None:
        web = actor.ability_to(BrowseTheWeb)
        email = self.email or unique_email(actor.name)
        web.app.auth.open().register(email, PASSWORD)
        actor.memory["email"] = email


class PlaceOrder:
    def __init__(self, side: str, price: str, quantity: str, symbol: str = "ETH-USDT"):
        self.order = OrderData(side, price, quantity, symbol)

    def perform_as(self, actor: Actor) -> None:
        web = actor.ability_to(BrowseTheWeb)
        created = web.app.dashboard.order_form.place(**asdict(self.order))
        actor.memory["last_order_id"] = created["id"]
```

```python
# ui_framework/screenplay/questions.py
class AvailableBalance:
    def __init__(self, asset: str):
        self.asset = asset

    def answered_by(self, actor: Actor) -> Locator:
        return actor.ability_to(BrowseTheWeb).app.dashboard.balances.available(self.asset)


class LastOrderStatus:
    def answered_by(self, actor: Actor) -> Locator:
        order_id = actor.memory["last_order_id"]
        return actor.ability_to(BrowseTheWeb).app.dashboard.orders.row(order_id).status
```

Question возвращает **Locator** — проверку делает тест через `expect` (как в PO, U4.1).
В «настоящем» Screenplay есть ещё `actor.should_see_the(question, matcher)` — для Playwright
естественнее оставить `expect`.

`actor.memory` — место, где актор хранит то, что узнал по ходу: id ордера, email. В PO состояние —
антипаттерн (U4.1), а в Screenplay это **память участника**, и она явная: задача пишет, вопрос читает.

---

## 3. Сила Screenplay: несколько каналов и участников

Ability можно добавить любую:

```python
alice = Actor("Алиса").can(BrowseTheWeb(page), CallTheApi(api_client))

alice.attempts_to(RegisterViaApi(), DepositViaApi("USDT", "1000"))   # подготовка через API — быстро
alice.attempts_to(PlaceOrder("BUY", "100", "1"))                     # проверяемое действие — через UI
```

Задачи, которым всё равно, UI это или API, переиспользуются; сценарии с несколькими пользователями
читаются естественно. (API внутри Playwright — U5.)

---

## 4. Page Object или Screenplay

| | Page Object | Screenplay |
|---|---|---|
| Единица | экран / компонент | задача, вопрос, участник |
| Порог входа | низкий, знают все | выше: больше классов, нужно договориться о стиле |
| Код | меньше | больше: класс на задачу и вопрос |
| Несколько пользователей | несколько PO / context — ок, но тест знает про страницы | естественно: акторы |
| UI + API в одном сценарии | отдельные клиенты рядом с PO | способности одного актора |
| Переиспользование | на уровне экранов | на уровне бизнес-действий |
| Риск | «God object», раздутые страницы | взрыв мелких классов, «архитектура ради архитектуры» |

Практичный ответ на собесе: **PO — основа**, она есть почти в каждом проекте. Screenplay —
когда сценарии многошаговые, участников несколько и действия идут через разные каналы. Часто
делают гибрид: PO и компоненты внизу, поверх — слой бизнес-шагов (по сути tasks), а тесты
используют шаги.

Наш фреймворк уже «гибридный»: фикстуры состояния (`logged_in_app`, `new_app`) и хелперы сценариев —
это и есть слой задач, только без классов.

---

## 5. Каркас UI-фреймворка: чек-лист готовности

Это артефакт модуля U4 — то, что показываешь на собесе («расскажите про ваш фреймворк»)
и что должно работать у другого человека с нуля.

**Запуск**
- [ ] README фреймворка: установка (`uv sync`, `playwright install` / `--browser-channel chrome`),
      запуск стенда, запуск тестов, окружения, Allure;
- [ ] `uv run pytest tests/ui` зелёный на docker;
- [ ] `ENV=stage uv run pytest tests/ui -m smoke` — запускается (падения от 5% сбоев допустимы и объяснимы);
- [ ] отчёт Allure собирается: шаги, скриншот при падении, окружение.

**Структура**
- [ ] `config/`, `pages/`, `components/`, `fixtures/`, `data/`, `utils/` — каждая папка с понятной ролью;
- [ ] зависимости в одну сторону (U4.4, раздел 7), нет циклических импортов;
- [ ] фикстуры фреймворка подключены через `pytest_plugins`, conftest тестов маленький.

**Page Object и компоненты**
- [ ] в тестах нет `page.get_by_*` / `page.locator`;
- [ ] в PO нет бизнес-проверок; методы для проверок отдают Locator;
- [ ] компоненты ищут только внутри root;
- [ ] переходы между экранами возвращают PO;
- [ ] страницы тест получает через `Application`; в нём нет сценариев и состояния.

**Данные и стабильность**
- [ ] уникальные данные на тест; цены не пересекаются с чужими ордерами;
- [ ] уборка за собой; уборка не падает на «уже убрано»;
- [ ] нет `sleep`, `networkidle`, `force=True`; хелперы ждут ответ сервера, а не тост (U2.1);
- [ ] `--count 5` на ключевых тестах — зелёный.

**Конфиг и секреты**
- [ ] адреса и таймауты — в env-файлах; секретов нет в git;
- [ ] `--base-url` перекрывает конфиг.

**Отчёт**
- [ ] `@allure.step` на методах PO, без паролей; метки feature/story/severity на тестах.

---

## 6. Шпаргалка по модулю U4

- **PO (U4.1)**: класс на экран; «как» в PO, «что» в тесте; локаторы атрибутами (ленивые);
  переходы возвращают PO; проверки — Locator для `expect`; в PO только синхронизация и проверка
  своего действия; отдельные методы для негативных сценариев. `Application` — композиция страниц
  на одном `page` через `cached_property`, одна фикстура `app` вместо фикстуры на каждую страницу.
- **Компоненты (U4.2)**: root-локатор, поиск только внутри; страница = композиция; строка таблицы —
  компонент; общая `Table` с колонкой по заголовку; компоненты не знают о страницах; модалка —
  компонент, метод открытия возвращает его.
- **Фикстуры и конфиг (U4.3)**: фикстуры состояния (`logged_in_app`) и фабрики (`new_app`); `yield`-уборка в обратном порядке;
  `request` и маркеры с данными; параметризованные фикстуры и `indirect`; autouse — только настройка;
  фикстуры в пакете через `pytest_plugins`; pydantic-settings, `ENV`, env-файлы, приоритет источников,
  `SecretStr`; перекрытие `base_url`.
- **Утилиты и отчёт (U4.4)**: utils не знают о page; Decimal из строки; `format_amount` как сервер;
  frozen dataclass для данных; `wait_until` на monotonic; Allure — шаги декоратором, скриншот хуком,
  метки, окружение; зависимости в одну сторону.
- **Screenplay (U4.5)**: актор, способности, задачи, вопросы; сила — несколько участников и каналов;
  PO — основа, Screenplay или гибрид — по сложности сценариев.

---

## Собес: банк вопросов по модулю U4

Весь банк модуля — разделы «Собес» уроков U4.1 (7 вопросов), U4.2 (6), U4.3 (7), U4.4 (6) и новые ниже (5).

**1. Что такое Screenplay и чем он отличается от Page Object?**
> Screenplay описывает сценарий через участников: актор со способностями — браузер, API — выполняет
> задачи, то есть бизнес-действия, и задаёт вопросы о состоянии системы. Page Object описывает экраны.
> PO проще и меньше кода; Screenplay лучше масштабируется на многошаговые сценарии с несколькими
> участниками и каналами — UI и API в одном тесте, — и переиспользует бизнес-действия, а не экраны.
> Цена — больше классов и выше порог входа.

**2. Что выберешь для нового проекта?**
> Page Object с компонентами как основу — его знает любой в команде. Поверх, когда сценарии становятся
> длинными, — слой бизнес-шагов. Полный Screenplay — если много ролей и сценариев «UI плюс API»,
> и команда готова поддерживать больше абстракций. Решаю по сложности сценариев, а не по моде.

**3. Расскажи про свой UI-фреймворк** (главный вопрос, 2–3 минуты).
> План ответа: стек (Python, pytest, Playwright, pydantic-settings, Allure) → слои снизу вверх
> (конфиг, утилиты и данные, компоненты, страницы, фикстуры, тесты) → как обеспечена стабильность
> (web-first проверки, хелперы ждут ответ сервера, изоляция данных, уборка) → окружения и секреты →
> отчётность → одно решение, которым гордишься, и одно, которое переделал бы.
> Готовая версия — твоя, в задаче 6.

**4. Как добавить в фреймворк новую страницу?**
> Если есть повторяющиеся блоки — сначала компоненты с root. Потом PO страницы: path, root, компоненты,
> переходы, `wait_loaded`. Свойство в `Application` — отдельная фикстура не нужна. Шаги Allure на публичных методах.
> Тест — только через PO. Если страница открывается из другой — метод перехода возвращает новый PO.

**5. Как поймёшь, что Page Object стал плохим?**
> Сотни строк и десятки методов, методы на каждый клик или наоборот на целый тест, проверки внутри,
> состояние, зашитые данные, тесты лезут в `page` мимо PO, правка одной кнопки ломает много мест.
> Лечу разбиением на компоненты и разделением экранов.

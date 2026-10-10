# U5. Урок 2 — тестовые данные

Задания: `practice/tasks/test_u5_02_test_data.py`, решение — `tests/ui/test_u5_02_test_data.py` (создаёшь сам), код — `ui_framework/data/`, `tests/ui/data/`.

План: стратегии данных (seed или генерация на тест); Faker и его ловушки; фабрики «пользователь /
пользователь с балансом / с ордерами»; builder; уникальность при параллельном запуске и префикс
прогона; данные из JSON/CSV для `parametrize`; уборка — через API, по префиксу через SQL;
файлы и `tmp_path`; общий стенд с чужими данными.

---

## 1. Стратегии данных

| | Статичные (seed) | Генерируемые на тест |
|---|---|---|
| Что | заранее созданные пользователи и справочники | тест создаёт всё, что ему нужно |
| Плюсы | быстро; есть «тяжёлые» данные (история за год) | изоляция; тесты независимы; можно параллельно |
| Минусы | тесты делят данные → ломают друг друга; seed «портится» | дольше (лечится API); мусор (лечится уборкой) |
| Когда | **только чтение**: справочники, отчёты, большие объёмы | **всё, что меняет состояние** |

Правило по умолчанию: **каждый тест создаёт своё**. Seed — осознанное исключение для read-only тестов.

### Seed должен быть идемпотентным

Запускается перед каждым прогоном и не должен ломаться от того, что данные уже есть:

```python
def ensure_user(api, email, password) -> ExchangeApi:
    r = api.ctx.post("/auth/register", data={"email": email, "password": password})
    if r.status not in (201, 409):                 # 409 email_taken — уже есть, это ок
        raise AssertionError(r.text())
    api.login(email, password)
    return api


def ensure_balance(api, asset, target: Decimal) -> None:
    current = next(to_decimal(b["available"]) for b in api.balances() if b["asset"] == asset)
    if current < target:
        api.deposit(asset, str(target - current))  # довести до нужного, а не «добавить ещё»
```

«Довести до» вместо «добавить» — иначе каждый прогон увеличивает баланс seed-пользователя.

---

## 2. Faker

```python
from faker import Faker

fake = Faker("ru_RU")
fake.name(), fake.email(), fake.password(length=12), fake.date_of_birth(), fake.city()
```

### Ловушка 1: плагин pytest сидирует каждый тест одинаково

Faker ставит **pytest-плагин** с фикстурой `faker`. Он сидирует генератор **нулём перед каждым тестом**
— поэтому значения в разных тестах **совпадают**. Проверено у нас:

```
test_a: achang@example.org  tn8Em4__*%zP
test_b: achang@example.org  tn8Em4__*%zP
```

Второй тест регистрации получит 409. Сид меняется фикстурой `faker_seed`, но для уникальных полей
это не решение.

### Ловушка 2: Faker не гарантирует уникальность

Даже без сида — на тысячах прогонов будут повторы. `fake.unique.email()` уникален только **внутри
одного процесса** и падает, когда варианты кончаются.

Итого: **уникальное поле — из uuid** (с читаемым префиксом), Faker — для «декоративных» полей,
где совпадение ничего не ломает. Воспроизводимость Faker (сид) полезна, когда нужно повторить
упавший тест с теми же данными — тогда сид печатают в лог.

---

## 3. Фабрики

Фабрика — функция, которая создаёт **готовый объект нужного состояния** со значениями по умолчанию:

```python
@dataclass
class Trader:
    email: str
    password: str
    api: ExchangeApi
    orders: list[dict] = field(default_factory=list)


def create_trader(ctx, password, balance: dict[str, str] | None = None,
                  orders: list[OrderData] = ()) -> Trader:
    email = unique_email("trader")
    api = ExchangeApi(ctx)
    api.register(email, password)
    api.login(email, password)
    for asset, amount in (balance or {}).items():
        api.deposit(asset, amount)
    created = [api.place_order(o) for o in orders]
    return Trader(email, password, api, created)


trader = create_trader(ctx, pw)                                         # просто пользователь
rich = create_trader(ctx, pw, balance={"USDT": "1000"})                 # с балансом
busy = create_trader(ctx, pw, balance={"USDT": "1000"},
                     orders=[OrderData(price="10"), OrderData(price="20")])   # с ордерами
```

Как фикстура — фабрика с уборкой (U4.3, U5.1): запоминает созданных и после теста отменяет их ордера.

Библиотеки: `factory_boy`, `polyfactory` — генерируют модели по описанию. Для API-подготовки
часто проще своя функция, как выше.

---

## 4. Builder

Когда вариантов много и важен порядок шагов, фабрика с десятком аргументов становится нечитаемой.
Builder — пошаговая сборка:

```python
class TraderBuilder:
    def __init__(self, ctx, password):
        self._ctx, self._password = ctx, password
        self._balance: dict[str, str] = {}
        self._orders: list[OrderData] = []

    def with_balance(self, asset: str, amount: str) -> "TraderBuilder":
        self._balance[asset] = amount
        return self

    def with_order(self, order: OrderData) -> "TraderBuilder":
        self._orders.append(order)
        return self

    def create(self) -> Trader:
        return create_trader(self._ctx, self._password, self._balance, self._orders)


seller = (TraderBuilder(ctx, pw)
          .with_balance("ETH", "2")
          .with_order(OrderData(side="SELL", price="350", quantity="2"))
          .create())
```

| | Фабрика с kwargs | Builder |
|---|---|---|
| Мало вариантов | ✅ проще | лишний класс |
| Много опций, шаги в порядке | аргументов слишком много | ✅ читается как описание |
| Python-идиома | ✅ значения по умолчанию, `replace()` | реже, но уместен для сложных объектов |

---

## 5. Уникальность при параллельном запуске и префикс прогона

uuid уникален и в параллели. Но для отладки и уборки полезен **читаемый префикс**:

```python
RUN_ID = os.getenv("TEST_RUN_ID") or datetime.now().strftime("%m%d%H%M%S")
WORKER = os.getenv("PYTEST_XDIST_WORKER", "gw0")        # при запуске через xdist (U5.3)


def unique_email(role: str = "user") -> str:
    return f"ui_{RUN_ID}_{WORKER}_{role}_{uuid4().hex[:6]}@test.com"
```

- по email сразу видно: какой прогон, какой воркер, какая роль;
- по префиксу `ui_{RUN_ID}_` можно найти и удалить **все** данные прогона;
- `RUN_ID` в CI задают снаружи (номер сборки), чтобы все воркеры использовали **один**.
  Без этого каждый процесс xdist посчитает своё время запуска.

---

## 6. Данные из JSON / CSV для parametrize

Табличные кейсы удобнее держать файлом — их правит и аналитик, и тестировщик без кода:

`tests/ui/data/invalid_orders.json`:

```json
[
  {"id": "пустая цена",          "price": "",    "quantity": "1", "field": "price"},
  {"id": "отрицательная цена",   "price": "-1",  "quantity": "1", "field": "price"},
  {"id": "нулевое количество",   "price": "10",  "quantity": "0", "field": "quantity"}
]
```

```python
DATA = Path(__file__).parent / "data"


def load_cases(name: str) -> list:
    cases = json.loads((DATA / name).read_text(encoding="utf-8"))
    return [pytest.param(c, id=c["id"]) for c in cases]


@pytest.mark.parametrize("case", load_cases("invalid_orders.json"))
def test_invalid_order(dashboard, case): ...
```

CSV — `csv.DictReader`; все значения придут **строками** (для нашего стенда это даже удобно — суммы и так строки).

Где лежат: файлы **кейсов** конкретных тестов — рядом с тестами (`tests/ui/data/`); **модели**
и генераторы — во фреймворке (`ui_framework/data/`). Загрузка — при сборке тестов (на уровне модуля),
поэтому `tmp_path` и фикстуры тут недоступны.

---

## 7. Уборка

| Способ | Когда |
|---|---|
| через API в `yield`-фикстуре | основной: тест убирает своё (U5.1) |
| «каждый тест создаёт своё» + уникальные данные | мусор остаётся, но не мешает — если ресурс не общий |
| **по префиксу** после прогона | когда API удаления нет, или тест упал до уборки |
| пересоздание окружения | эфемерный стенд на прогон — лучший вариант, если есть |

### По префиксу через SQL

У стенда нет API удаления пользователя. Тестовое окружение — наше, база доступна
(`postgresql://exchange:exchange@localhost:5432/exchange`, модуль F3). Внешние ключи **без каскада**,
поэтому порядок важен — сначала зависимые таблицы:

```python
def delete_users_by_prefix(dsn: str, prefix: str) -> int:
    pattern = prefix + "%"
    with psycopg.connect(dsn) as conn:
        ids = "SELECT id FROM users WHERE email LIKE %s"
        for table in ("idempotency_keys", "orders", "balances"):
            conn.execute(f"DELETE FROM {table} WHERE user_id IN ({ids})", (pattern,))
        return conn.execute("DELETE FROM users WHERE email LIKE %s", (pattern,)).rowcount
```

Правила: **только** в окружениях, где это разрешено (docker, local — да; общий stage — нет:
флаг в Settings); префикс должен быть **достаточно узким** — `ui_0910153000_`, а не `ui_`;
вызывать в session-teardown или отдельной командой. Значения — параметрами (`%s`), не f-строкой.

---

## 8. Файлы и `tmp_path`

```python
def test_export(tmp_path):                         # своя временная папка на тест
    path = tmp_path / "orders.csv"
    ...


@pytest.fixture(scope="session")
def shared_dir(tmp_path_factory):                  # на весь прогон
    return tmp_path_factory.mktemp("exports")
```

- pytest создаёт папку сам, хранит последние 3 прогона (`/tmp/pytest-of-<user>/`), чистить руками не нужно;
- в папку проекта файлы тестов **не пишут** — мусор в git, конфликты в параллели;
- генерация файлов для загрузки: CSV — модуль `csv`; картинка — `page.screenshot(path=...)` или
  Pillow; большой файл — `path.write_bytes(os.urandom(5 * 1024 * 1024))`.
  Загрузка через `set_input_files` — в U3 (на стенде загрузки нет).

---

## 9. Общий стенд с чужими данными

То, что мы видели в U1.4: в стакане висят чужие ордера, наш исполнился об них.
- не полагаться на «пусто»: проверять **свои** данные (свой пользователь, свой id), а не «в системе 0 ордеров»;
- данные, которые **не пересекаются** с чужими: уникальные имена, цены в «своём» диапазоне;
- если пересечение неизбежно — изолированное окружение (своя база, docker на прогон) или
  отдельный тенант / префикс;
- убирать за собой — чтобы не быть «чужими данными» для других.

---

## Собес: вопросы и ответы

**1. Как вы готовите тестовые данные?**
> По умолчанию каждый тест создаёт своё через API: фабрики «пользователь», «с балансом», «с ордерами»,
> уникальные поля из uuid с префиксом прогона. Статичный seed — только для read-only тестов и идемпотентный:
> «создать, если нет» и «довести до нужного значения». Табличные кейсы — в JSON/CSV для parametrize.

**2. Как чистите данные?**
> Тест убирает своё через API в teardown фикстуры. Если удалить через API нельзя или тест упал до уборки —
> уборка по префиксу прогона после завершения, на тестовом окружении можно напрямую в базе с учётом
> внешних ключей. Лучший вариант — эфемерное окружение на прогон, которое просто удаляется.

**3. Общий стенд с чужими данными — что делать?**
> Не полагаться на пустое состояние, проверять только свои сущности по id. Делать данные, которые не
> пересекаются с чужими. Убирать за собой. Если этого мало — добиваться изолированного окружения
> или отдельного тенанта.

**4. Faker — плюсы и подводные камни?**
> Удобно генерировать правдоподобные данные и локали. Но уникальность он не гарантирует, а pytest-плагин
> по умолчанию сидирует каждый тест одинаково — значения в разных тестах совпадают. Поэтому ключевые поля
> делаю из uuid, Faker — для декоративных, сид печатаю, если нужна воспроизводимость.

**5. Фабрика или builder?**
> Для небольшого числа вариантов — функция-фабрика со значениями по умолчанию, это идиоматично для Python.
> Builder — когда опций много и важна последовательность шагов: читается как описание объекта.

**6. Как обеспечить уникальность при параллельном запуске?**
> uuid в ключевых полях. Плюс читаемый префикс: id прогона, общий для всех воркеров, и id воркера —
> чтобы по данным было видно, откуда они, и чтобы можно было убрать всё за прогон.
> Никаких общих фиксированных имён и счётчиков в файлах.

**7. Где хранить данные для параметризации?**
> Кейсы — в JSON или CSV рядом с тестами, загружаю при сборке и превращаю в `pytest.param` с читаемыми id.
> Модели и генераторы — во фреймворке. Временные файлы — в `tmp_path`, не в папке проекта.

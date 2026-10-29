# C1 · Раздел 10. Где это ломает автотесты

[← раздел 9](../s09_hashable/THEORY.md) · [оглавление урока](../README.md) · [раздел 11 →](../s11_cheatsheet/THEORY.md)

**Общий шаблон данных и поверхностная копия.**

```python
BASE_USER = {"email": "a@b.c", "roles": ["user"]}

def test_admin():
    user = BASE_USER.copy()           # поверхностная: roles — общий список!
    user["roles"].append("admin")     # испортили BASE_USER для всех

def test_regular_user():
    assert BASE_USER["roles"] == ["user"]   # падает, если test_admin шёл раньше
```

Фикс: `copy.deepcopy(BASE_USER)` или фабрика `make_user()`, которая каждый раз строит новый dict.

**Фикстура с широким scope отдаёт изменяемый объект.**

```python
@pytest.fixture(scope="session")
def default_order():
    return {"symbol": "BTC/USDT", "qty": "1"}
# один объект на весь прогон: тест, который сделал default_order["qty"] = "0",
# сломает все тесты после себя
```

Фикс: `scope="function"` для изменяемых данных или отдавать копию.

**Мок хранит ссылку, а не снимок.**

```python
from unittest.mock import Mock

client = Mock()
payload = {"qty": 1}
client.post(payload)
payload["qty"] = 5
print(client.post.call_args)   # call({'qty': 5}) — «история» изменилась задним числом
```

Проверку `assert_called_with` делай до того, как меняешь объект, или передавай копию
(задача t10 — свой записыватель вызовов со снимками).

**Хелпер со значением по умолчанию.** `def create_user(roles=[])` или
`def make_order(ts=datetime.now())` — данные «протекают» между тестами или время замерзает.

**Как распознать.** Тест проходит сам по себе (`pytest -k test_x`), но падает в общем прогоне
или при другом порядке тестов. Первым делом ищи общий изменяемый объект: модульную
константу-словарь, фикстуру с `scope="session"` или `"module"`, значение по умолчанию.

---

### Практика к разделу

Все команды — из папки `c01_objects`.

- **Упражнения:** `drills.py` в этой папке — впиши ответы под фрагментами, проверка: `uv run python s10_autotests/drills.py`
- **Задача:** `t10_call_recorder.py` в этой папке — проверка: `uv run pytest -k t10`
- **Quiz урока:** №15 в `quiz.py` — проверка: `uv run python quiz.py 15`

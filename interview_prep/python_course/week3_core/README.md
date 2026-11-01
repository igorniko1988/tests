# Неделя 3 · минимум

11 ключевых задач недели 3 в одной папке — копии из `week3/`, решай здесь.
Команды — из папки `interview_prep/python_course/week3_core`. Тесты одной задачи: `uv run pytest -k c07_t01`.
Теория — `THEORY.md` в папке урока `week3/<урок>/`.

| # | Файл | О чём | Урок |
|---|---|---|---|
| 1 | `c07_t01_user.py` | класс, `@property` с валидацией | `week3/c07_classes` |
| 2 | `c07_t02_order_from_json.py` | `@classmethod` — конструктор из ответа API | там же |
| 3 | `c08_t01_client_hierarchy.py` | наследование, `super()` | `week3/c08_inheritance` |
| 4 | `c08_t03_abstract_page.py` | абстрактный базовый класс (Page Object) | там же |
| 5 | `c09_t02_cart.py` | `__len__`, `__iter__`, `__contains__` | `week3/c09_magic_methods` |
| 6 | `c09_t05_hashable_ticker.py` | `__eq__` + `__hash__`, объекты в set | там же |
| 7 | `q3_t01_lru_cache.py` | LRU cache на `OrderedDict` | `week3/q3_class_design` |
| 8 | `q3_t02_rate_limiter.py` | rate limiter, скользящее окно на deque | там же |
| 9 | `a06_t01_merge_intervals.py` | сортировка + слияние интервалов | `week3/a06_sorting_intervals` |
| 10 | `a07_t01_binary_search.py` | бинарный поиск | `week3/a07_binary_search` |
| 11 | `a08_t02_subarray_sum_k.py` | префиксные суммы + dict | `week3/a08_prefix_sums` |

Тесты LRU «руками» (t06) помечены skipped — эта задача не входит в минимум.
Всё сразу: `uv run pytest`. Эталон: `SRC=solutions uv run pytest`.

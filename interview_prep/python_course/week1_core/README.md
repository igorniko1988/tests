# Неделя 1 · минимум для закрытия

13 главных задач недели 1 и контрольная в одной папке. Это копии задач из `week1/`:
решай здесь, оригиналы в `week1/` не трогай. Остальные задачи недели — потом, если будет время.

Все команды — из папки `interview_prep/python_course/week1_core`.
Перед кодом впиши комментарием вход, выход и типы. Застрял на 20 минут — «покажи решение».

| # | Файл | Задача | Тесты | Теория |
|---|---|---|---|---|
| 1 | `a2_t01_two_sum.py` | индексы пары с суммой target, O(n) | `uv run pytest -k a2_t01` | `week1/a2_hashing/README.md` |
| 2 | `a2_t02_is_anagram.py` | анаграммы через подсчёт символов | `uv run pytest -k a2_t02` | там же |
| 3 | `a2_t03_group_anagrams.py` | группировка, ключ `tuple(sorted(word))` | `uv run pytest -k a2_t03` | там же |
| 4 | `a2_t04_first_repeated.py` | первый повтор через `seen = set()` | `uv run pytest -k a2_t04` | там же |
| 5 | `a1_t01_reverse_words.py` | split / join | `uv run pytest -k a1_t01` | `week1/a1_arrays_strings/README.md` |
| 6 | `a1_t02_move_zeros.py` | два указателя на месте | `uv run pytest -k a1_t02` | там же |
| 7 | `a1_t04_max_profit.py` | один проход, держим минимум | `uv run pytest -k a1_t04` | там же |
| 8 | `a1_t06_compress.py` | `"aaabb"` → `"a3b2"` | `uv run pytest -k a1_t06` | там же |
| 9 | `q1_t02_json_diff.py` | разница двух ответов API | `uv run pytest -k q1_t02` | `week1/q1_data/README.md` |
| 10 | `q1_t04_orders_summary.py` | группировка, Decimal, сортировка | `uv run pytest -k q1_t04` | там же |

## Контрольная X1 — в конце, по таймеру

| Часть | Файл | Проверка |
|---|---|---|
| 1. Вопросы устно | `x1_questions.md` | ответить вслух, потом «проверь X1 вопросы» |
| 2. Что выведет | `x1_output/drills.py` | `uv run python x1_output/drills.py` |
| 3. Алгоритмы | `x1_t01_pair_difference.py`, `x1_t02_decode.py` | `uv run pytest -k x1_t01`, `-k x1_t02` |
| 4. AQA | `x1_t03_compare_responses.py` | `uv run pytest -k x1_t03` |

Всё сразу: `uv run pytest`. Эталон: `SRC=solutions uv run pytest`.

# Live coding на Python: от простого к сложному

Цель: на собесе спокойно решать задачи уровня LeetCode Easy и Medium,
вслух объяснять решение и сложность, писать чистый код без подсказок IDE.

## Как устроен курс

Курс идёт по **паттернам**, а не по случайным задачам. Почти любая задача
на собесе сводится к одному из 15 приёмов. Если узнаёшь приём, решение
находится за минуты.

Каждый модуль:
- `lesson.py` — теория маленькими кусками: код, результат, «что выведет»;
- `tasks/` — 10 задач: 3 разминка, 5 основных, 2 сложных (звёздочка);
- `tests/` — тесты на каждую задачу, включая граничные случаи;
- `solutions/` — эталон. Не открывать, пока не решил сам.

Начиная с модуля 3, в каждом модуле есть 1–2 задачи на прошлые темы, чтобы
старое не забывалось.

## Как решать задачу (тренируем каждый раз)

1. Перескажи условие своими словами, спроси про граничные случаи:
   пустой вход, один элемент, дубли, отрицательные числа, регистр.
2. Разбери 1–2 примера руками.
3. Скажи простое решение «в лоб» и его сложность.
4. Найди улучшение: какой паттерн подходит?
5. Пиши код, проговаривая.
6. Прогони пример глазами по коду, потом граничные случаи.
7. Назови сложность по времени и памяти.

## Программа

| #  | Модуль | Паттерн / тема | Примеры задач |
|----|--------|----------------|---------------|
| 1  | m01_arrays_strings | Big-O, списки и строки, идиомы Python | reverse words, move zeros, merge sorted |
| 2  | m02_hashing | dict, set, Counter, defaultdict | two sum, group anagrams, first unique |
| 3  | m03_two_pointers | Два указателя | valid palindrome, 3sum, container with water |
| 4  | m04_sliding_window | Скользящее окно | longest substring без повторов, max sum k |
| 5  | m05_stack_queue | Стек, очередь, deque | скобки, min stack, daily temperatures |
| 6  | m06_sorting_intervals | sorted(key=...), интервалы | merge intervals, meeting rooms |
| 7  | m07_binary_search | Бинарный поиск | search insert, rotated array, sqrt |
| 8  | m08_prefix_sums | Префиксные суммы | subarray sum = k, range sum |
| 9  | m09_recursion | Рекурсия, backtracking | flatten, subsets, permutations |
| 10 | m10_linked_lists | Связные списки | reverse, cycle, merge two lists |
| 11 | m11_trees | Деревья, DFS и BFS | max depth, level order, validate BST |
| 12 | m12_graphs | Графы, BFS по сетке | number of islands, shortest path |
| 13 | m13_heaps | heapq, top-k | k most frequent, merge k sorted |
| 14 | m14_dp | Динамическое программирование | climbing stairs, coin change, LIS |
| 15 | m15_aqa_practical | Задачи «из жизни» AQA | парсинг логов, flatten JSON, retry, LRU cache, rate limiter |
| 16 | m16_mock | Пробные лайвкодинги на время | 2 задачи за 45 минут с разбором |

## Запуск

Из папки модуля:

    cd interview_prep/livecoding_python/m01_arrays_strings
    uv run python lesson.py            # урок
    uv run pytest -q -k t03            # одна задача
    uv run pytest -q                   # весь модуль

Проверить тесты на эталоне (для Claude): `SRC=solutions uv run pytest -q`.

Решил задачу — пиши в чат «готово t03». Claude прогонит тесты, сделает
ревью как интервьюер и задаст 1–2 вопроса, которые задали бы на собесе.

## Визуализации

Разбор решения идёт с пошаговым визуализатором: подсвечена строка кода,
видны переменные и история шагов. Файлы лежат в `<модуль>/visual/`,
открываются в браузере (`open visual/t02_compress.html`).

- t02 compress: https://claude.ai/artifact/Az7JJPTVcBMREakNebWSbo

Шпаргалка по выбору паттерна: `PATTERNS.md`, интерактивное дерево решений: `pattern_picker.html` (https://claude.ai/artifact/WHT6kR9Rphaw4pznTSNQAk).

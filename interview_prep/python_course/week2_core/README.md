# Неделя 2 · минимум

13 ключевых задач недели 2 в одной папке — копии из `week2/`, решай здесь.
Команды — из папки `interview_prep/python_course/week2_core`. Тесты одной задачи: `uv run pytest -k a03_t01`.
Теория — `THEORY.md` в папке урока `week2/<урок>/`.

| # | Файл | О чём | Урок |
|---|---|---|---|
| 1 | `a03_t01_valid_palindrome.py` | два указателя с краёв | `week2/a03_two_pointers` |
| 2 | `a03_t02_two_sum_sorted.py` | two sum на отсортированном, указатели | там же |
| 3 | `a03_t05_remove_duplicates.py` | удаление дублей на месте (как move_zeros) | там же |
| 4 | `a04_t01_max_sum_k.py` | окно фиксированной длины | `week2/a04_sliding_window` |
| 5 | `a04_t02_longest_unique.py` | окно переменной длины + set | там же |
| 6 | `a05_t01_valid_parentheses.py` | стек | `week2/a05_stack_queue` |
| 7 | `c04_t01_make_counter.py` | замыкание, `nonlocal` | `week2/c04_functions` |
| 8 | `c05_t02_error_lines.py` | генератор по большому логу | `week2/c05_generators` |
| 9 | `c05_t03_batched.py` | генератор пачек | там же |
| 10 | `c06_t01_timer.py` | простой декоратор, `wraps` | `week2/c06_decorators` |
| 11 | `c06_t03_retry.py` | декоратор с параметрами | там же |
| 12 | `q2_t06_wait_until.py` | ожидание условия с таймаутом (AQA) | `week2/q2_function_utils` |

Всё сразу: `uv run pytest`. Эталон: `SRC=solutions uv run pytest`.

"""
F1. Урок 4 — генераторы, yield и контекстные менеджеры.

Теория: practice/f1_04_generators.md
Запуск: uv run python practice/f1_04_generators.py

Задача 1. Первый генератор.
    Генератор order_ids(prefix, count) отдаёт строки вида "ORD-1", "ORD-2", ... (prefix + номер).
    Переберите его в for. Потом создай генератор заново и достань 2 значения через next().
    Что будет при третьем next(), если count=2?

Задача 2. Генератор vs список.
    Сравни размер в памяти: sys.getsizeof([x for x in range(1_000_000)])
    и sys.getsizeof((x for x in range(1_000_000))). Выведи оба числа.
    Потом попробуй пройти один и тот же генератор двумя for подряд — что во втором?

Задача 3. Постраничный перебор (имитация API).
    Есть «сервер» — список страниц:
        PAGES = [["o1", "o2"], ["o3", "o4"], ["o5"]]
    Функция fetch_page(number) возвращает PAGES[number] и печатает "загружаю страницу N".
    Генератор all_orders() перебирает страницы по одной через fetch_page и отдаёт ордера
    по одному (yield from). Проверь: возьми только первые 3 ордера (break после третьего) —
    сколько страниц загрузилось? Должно быть 2, а не 3 — в этом ленивость.

Задача 4. Контекстный менеджер-класс.
    Класс TestUser: в __enter__ печатает "создаю пользователя <email>" и возвращает self,
    в __exit__ печатает "удаляю пользователя <email>" и возвращает False.
    Проверь два случая: обычный with и with, внутри которого raise ValueError
    (оберни снаружи в try/except) — удаление должно напечататься в обоих случаях.

Задача 5. Контекстный менеджер через @contextmanager.
    Сделай то же самое, что в задаче 4, функцией test_user(email) с @contextmanager
    и try/finally. Тоже проверь оба случая.

Задача 6. Фикстура-генератор вручную (как это делает pytest).
    Напиши генератор fake_fixture(): печатает "setup", делает yield "данные", печатает "teardown".
    Сымитируй pytest без pytest: создай генератор, возьми значение через next() (это «до теста»),
    «выполни тест» (print), потом вызови next() ещё раз внутри try/except StopIteration
    (это «после теста»). Убедись, что teardown напечатался.

Вопросы собеса (ответь своими словами внизу файла):
    1. Чем yield отличается от return? Что вернёт вызов функции-генератора?
    2. Генератор или список — когда что? В чём минус генератора?
    3. Как работает фикстура pytest с yield? Выполнится ли код после yield, если тест упал?
    4. Что гарантирует with? Что такое __enter__ и __exit__?
    5. Что будет, если __exit__ вернёт True?
    6. Как написать контекстный менеджер без класса?
"""


# --- Задача 1 ---

def gen(prefix: str, count: int):

    gen = (prefix + f'-{number}' for number in range(count))
    return gen

    # calls = 0
    # result = []
    # while calls <= count:
    #     result.append(prefix + f'-{calls}')
    #     calls +=1
    # yield result

x = gen('number', 5)


# for pref in x:
#     print(pref)

print(next(x))
print(next(x))
print(next(x))




# --- Задача 2 ---
import sys

print(sys.getsizeof([x for x in range(10000)]))
print(sys.getsizeof((x for x in range(10000))))

# for x in (x for x in range(10000)):
#     print(x)

# for x in [x for x in range(10000)]:
#     print(x)

# --- Задача 3 ---
PAGES = [["o1", "o2"], ["o3", "o4"], ["o5"]]


def fetch_page(number):
    print(f'Loading the page {number} ')
    return PAGES[number]

def all_orders(number):
    g = (page for page in fetch_page(number))
    for gen in g:
        yield from gen

print(all_orders(1))

# --- Задача 4 ---

class TestUser:
    def __init__(self, email):
        self.email = email


    def __enter__(self):
        print(f'Printing test user with email {self.email}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'Deleting the user with email {self.email}')
        return False

with TestUser('niko@gmail.com') as user:
    print('magician')


# with TestUser('niko@gmail.com') as user2:
#     try:
#         print('magician')
#         raise ValueError('hiiii')
#     except Exception as e:
#         raise


# --- Задача 5 ---

from contextlib import contextmanager

@contextmanager
def prepare_user(user_email):
    print('this is start')
    try:
        yield
    finally:
        print('Goodbye')

with prepare_user('niko@gmai.com'):
    from time import sleep
    sleep(2)


# --- Задача 6 ---

@contextmanager
def fake_fixture(*args):
    print('setup')
    prepare_data = args
    try:
        yield prepare_user
    finally:
        print('teardown')

with fake_fixture(1,2,3,4,5):
    sleep(5)

# --- Ответы на вопросы собеса ---
# 1. Yield return the result and freezes till the next call of the function end its process
# 2. Lists stores all the data in the memory, generators stores only the last data
# 3. Yiels garanties that the code after yeild will be executed evein if the tests failed
# 4. with garanties that exit criteria will be executed
# 5. may be nothig will change its just the result of exit criteria
# 6. using contextmanager from contextlib, so by adding contextmanager decorater

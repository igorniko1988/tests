"""
F1. Урок 1 — классы и объекты.

Теория: practice/f1_01_classes.md
Запуск: uv run python practice/f1_01_classes.py

Задача 1. Баланс.
    Класс Balance:
    - __init__ принимает asset (строка, например "USDT") и available (число, по умолчанию 0);
    - метод deposit(amount) увеличивает available;
    - метод withdraw(amount) уменьшает available, а если денег не хватает —
      raise ValueError("недостаточно средств").
    Проверь: пополнить на 100, снять 30 -> available == 70; снять 1000 -> ValueError.

Задача 2. Два объекта независимы.
    Создай Balance("USDT") и Balance("BTC"), пополни только первый,
    выведи available обоих и убедись, что второй не изменился.

Задача 3. Атрибут класса.
    Добавь в Balance атрибут класса supported_assets = {"USDT", "BTC", "ETH"}.
    В __init__, если asset не из набора, — raise ValueError. Проверь на Balance("DOGE").

Задача 4. Книга ордеров.
    Класс OrderBook:
    - __init__ создаёт пустой список self.orders;
    - add(symbol, side, price, quantity) добавляет словарь с этими полями;
    - count() возвращает количество ордеров;
    - total_cost() возвращает сумму price * quantity по всем ордерам.
    Добавь 2 ордера и выведи count() и total_cost().

Задача 5 (со звёздочкой). Запусти код ниже, объясни результат и исправь:

    class Cart:
        items = []

        def add(self, item):
            self.items.append(item)

    a = Cart()
    b = Cart()
    a.add("apple")
    print(b.items)

Вопросы собеса (ответь своими словами в комментариях внизу файла):
    1. Чем класс отличается от объекта?
    2. Что такое self и почему его не передают при вызове метода?
    3. Когда вызывается __init__? Это конструктор?
    4. Чем атрибут класса отличается от атрибута объекта? Чем опасен изменяемый атрибут класса?
"""


# --- Задача 1 ---

class Balance:
    supported_asset = {'BTC','USDT','ETH'}

    def __init__(self, asset: str, available: int = 0):
        if asset not in self.supported_asset:
            raise ValueError('not supported asset')
        self.asset = asset
        self.available = available

    def deposit(self, value):
        self.available +=value

    def withdraw(self, value):
        if self.available < value:
            raise ValueError('not enough money')
        self.available -=value

alice = Balance('USDT')
alice.deposit(100)
alice.withdraw(30)
print(alice.available)

# --- Задача 2 ---

bob = Balance('BTC')
bob.deposit(20)
print(alice.available)
print(bob.available)


# --- Задача 3 ---
try:
    doge = Balance('DOGE')
except ValueError as error:
    print(f'Expected error {error}')
# --- Задача 4 ---

class OrderBook:
    def __init__(self):
        self.orders = []

    def add(self, symbol, side, price, quantity):
        self.orders.append({'symbol': symbol, 'side': side, 'price': price, 'quantity': quantity})

    def count(self):
        return len(self.orders)

    def total_cost(self):
        total_cost = 0
        for item in self.orders:
            cost_of_one_order = item['price'] * item['quantity']
            total_cost +=cost_of_one_order
        return total_cost

o1 = OrderBook()
o1.add('BTC','short',10,2)
o1.add('ETH','long',20,2)
print(o1.total_cost())

# --- Задача 5 ---
class Cart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)


a = Cart()
b = Cart()
a.add("apple")
print(b.items)

# Answear = the idea is that items list is common for both objects so in the operating memory after
# initiazlizn object we create common list and work with them with all objects that inheris class behavior

# --- Ответы на вопросы собеса ---
# 1. Class its construcotr, its like a template which is inherited by its objects
# 2. Its called automatically, its referance to the object
# 3. Its constructor its called after createing an object and in this stage object properties is saved
# 4. class atribbute is common for all its objects, object attribute is unique for each object. The dangeroucity is if one object changes class attributes the changes will affect all other objects


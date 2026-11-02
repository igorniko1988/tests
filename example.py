class Order:
    def __init__(self, symbol, qty, price):
        self.symbol, self.qty, self.price = symbol, qty, price
        self.__name = 'niko'

    @classmethod
    def from_json(cls):            # альтернативный конструктор
        return 1

    @staticmethod
    def is_valid_symbol():         # обычная функция, «живущая» в классе
        return 'asdsadas'

print(Order.from_json())
print(Order.is_valid_symbol())
order = Order('asdsad',22,213)
print(order._Order__name)
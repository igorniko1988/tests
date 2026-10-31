"""C8 · Наследование и проектирование — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки interview_prep/python_course/week3/c08_inheritance): uv run python drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {'11', '12', '13', '14'}  # доп. фрагменты: можно пропустить


D["1"] = """
class A:
    def who(self):
        return "A"

class B(A):
    pass

print(B().who(), isinstance(B(), A), issubclass(A, B))
"""
A["1"] = ""


D["2"] = """
class A:
    def __init__(self):
        self.x = 1

class B(A):
    def __init__(self):
        self.y = 2

b = B()
print(b.y, hasattr(b, "x"))
"""
A["2"] = ""


D["3"] = """
class A:
    def greet(self):
        return "A"

class B(A):
    def greet(self):
        return "B+" + super().greet()

print(B().greet())
"""
A["3"] = ""


D["4"] = """
class A:
    def hi(self):
        return ["A"]

class B(A):
    def hi(self):
        return ["B"] + super().hi()

class C(A):
    def hi(self):
        return ["C"] + super().hi()

class D(B, C):
    def hi(self):
        return ["D"] + super().hi()

print(D().hi())
"""
A["4"] = ""


D["5"] = """
class A: pass
class B(A): pass
class C(A): pass
class D(C, B): pass

print([k.__name__ for k in D.__mro__])
"""
A["5"] = ""


D["6"] = """
class A:
    def f(self):
        return "A"

class B:
    def f(self):
        return "B"

class C(B, A):
    pass

print(C().f())
"""
A["6"] = ""


D["7"] = """
from abc import ABC, abstractmethod

class Page(ABC):
    @abstractmethod
    def open(self): ...

Page()
"""
A["7"] = ""


D["8"] = """
from abc import ABC, abstractmethod

class Page(ABC):
    @abstractmethod
    def open(self): ...

class Login(Page):
    def open(self):
        return "opened"

print(Login().open())
"""
A["8"] = ""


D["9"] = """
class Duck:
    def quack(self):
        return "quack"

class Robot:
    def quack(self):
        return "beep"

print([x.quack() for x in (Duck(), Robot())])
"""
A["9"] = ""


D["10"] = """
class Log:
    def send(self):
        return "log+" + super().send()

class Client:
    def send(self):
        return "sent"

class LoggedClient(Log, Client):
    pass

print(LoggedClient().send())
"""
A["10"] = ""


# доп. — по желанию
D["11"] = """
class Client:
    def send(self):
        return "sent"

class Log:
    def send(self):
        return "log+" + super().send()

class Wrong(Client, Log):
    pass

print(Wrong().send())
"""
A["11"] = ""


# доп. — по желанию
D["12"] = """
class Base:
    def __init__(self, name):
        self.name = name

class Child(Base):
    pass

print(Child("x").name)
Child()
"""
A["12"] = ""


# доп. — по желанию
D["13"] = """
class A:
    def __init__(self):
        self.__secret = 1
        self._shared = 2

class B(A):
    def get(self):
        return self._shared, self.__dict__

print(B().get())
"""
A["13"] = ""


# доп. — по желанию
D["14"] = """
class A:
    x = "A"

class B(A):
    pass

B.x = "B"
print(A.x, B.x, A().x)
"""
A["14"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)

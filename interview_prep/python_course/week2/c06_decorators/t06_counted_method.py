"""C6 t06 (★ optional, ~25 min). A class decorator that also works on methods.

The CountCalls class from t04 breaks on methods:

    class Api:
        @CountCalls
        def get(self, path): ...

    Api().get("/x")   # TypeError: get() missing 1 required positional argument: 'path'

Implement a class Counted - the same counting decorator (attribute count, works on
functions) - that ALSO works on methods: self must be passed, and the count is shared
by all instances (it is one function in the class).

Hint: when a function is accessed through an instance, Python calls its __get__
(the descriptor protocol) to bind self. Implement __get__(self, instance, owner).

Example:
    class Api:
        @Counted
        def get(self, path):
            return f"GET {path}"

    a, b = Api(), Api()
    a.get("/x"), b.get("/y")   -> "GET /x", "GET /y"
    Api.get.count              -> 2

Follow-up questions:
- Why does a plain function decorator not have this problem?
- What does functools.partial(self, instance) return here?

Run (from interview_prep/python_course/week2/c06_decorators): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 6–7.
"""


class Counted:
    def __init__(self, func) -> None:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __get__(self, instance, owner):
        raise NotImplementedError

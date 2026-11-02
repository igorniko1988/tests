"""C8 t02 (required, ~15 min). Predict MRO and super() calls.

Do NOT run the code first. Read the classes below and fill in the two answers:

- ANSWER_MRO   - list of class names in Final.__mro__ (including "object");
- ANSWER_CALLS - the list that Final().setup() returns.

Then check with the tests. If you were wrong, explain in chat why.

Follow-up questions:
- Why does super() in Logged not call Base directly?

Run (from interview_prep/python_course/week3/c08_inheritance): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 4.
"""


class Base:
    def setup(self):
        return ["Base"]


class Logged(Base):
    def setup(self):
        return ["Logged"] + super().setup()


class Authorized(Base):
    def setup(self):
        return ["Authorized"] + super().setup()


class Retrying(Authorized):
    def setup(self):
        return ["Retrying"] + super().setup()


class Final(Logged, Retrying):
    def setup(self):
        return ["Final"] + super().setup()


ANSWER_MRO: list[str] = []
ANSWER_CALLS: list[str] = []

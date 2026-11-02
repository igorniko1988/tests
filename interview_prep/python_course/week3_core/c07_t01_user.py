"""C7 t01 (required, ~20 min). User model with validation in properties.

Implement a class User(name, email):

- name: a non-empty string after strip(); otherwise ValueError. Stored stripped.
- email: a property with a setter. Valid email: exactly one "@", non-empty parts on both
  sides, and a "." in the part after "@". Stored stripped and lowercase. Invalid -> ValueError.
  Validation also works on assignment: user.email = "bad" -> ValueError.
- domain: read-only property - the part after "@". Assigning to it -> AttributeError.

Example:
    u = User(" Ann ", " Ann@Mail.COM ")
    u.name, u.email, u.domain   -> "Ann", "ann@mail.com", "mail.com"
    u.email = "x@y.io"
    u.domain                    -> "y.io"
    User("Bob", "bob@mail")     -> ValueError

Follow-up questions:
- Why does the getter return self._email and not self.email?
- How does __init__ reuse the setter's validation?

Run (from interview_prep/python_course/week3_core): uv run pytest -k c07_t01
Теория: THEORY.md в этой папке, раздел 3.
"""


class User:
    def __init__(self, name: str, email: str) -> None:
        raise NotImplementedError

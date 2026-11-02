"""A5 t02 (required, ~20 min). Min stack.

Implement a class MinStack with all operations in O(1):
- push(x)    - put x on top;
- pop()      - remove and return the top; IndexError if empty;
- top()      - return the top without removing; IndexError if empty;
- get_min()  - return the minimum of all elements; IndexError if empty;
- len(s)     - number of elements.

Example:
    s = MinStack()
    s.push(5); s.push(2); s.push(7)
    s.get_min()  -> 2
    s.pop()      -> 7
    s.pop()      -> 2
    s.get_min()  -> 5

Follow-up questions:
- Why is one variable `self.min` not enough?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 5.
"""


class MinStack:
    def __init__(self) -> None:
        raise NotImplementedError

    def push(self, x) -> None:
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def top(self):
        raise NotImplementedError

    def get_min(self):
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

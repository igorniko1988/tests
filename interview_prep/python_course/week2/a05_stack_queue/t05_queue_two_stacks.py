"""A5 t05 (required, ~20 min). Queue via two stacks.

Implement a FIFO queue MyQueue using ONLY two Python lists used as stacks
(append and pop() from the end; no pop(0), no insert, no deque, no indexing other than [-1]).

Methods:
- push(x)   - add to the back;
- pop()     - remove and return the front; IndexError if empty;
- peek()    - return the front without removing; IndexError if empty;
- len(q)    - number of elements.

Requirements:
- Amortized O(1) per operation. Tests push and pop 200 000 items.

Example:
    q = MyQueue()
    q.push(1); q.push(2)
    q.peek()  -> 1
    q.pop()   -> 1
    q.push(3)
    q.pop(), q.pop()  -> 2, 3

Follow-up questions:
- When exactly do you move items from one stack to the other, and why only then?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 5.
"""


class MyQueue:
    def __init__(self) -> None:
        raise NotImplementedError

    def push(self, x) -> None:
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

"""A5 t04 (required, ~20 min). Evaluate reverse Polish notation.

Evaluate an expression in reverse Polish notation. tokens are integers (may be negative,
e.g. "-3") and operators + - * /. Division truncates toward zero (6 / -4 = -1).
The expression is always valid.

Examples:
    eval_rpn(["2", "1", "+", "3", "*"])          -> 9      # (2 + 1) * 3
    eval_rpn(["4", "13", "5", "/", "+"])         -> 6      # 4 + 13 / 5
    eval_rpn(["7", "-2", "/"])                   -> -3
    eval_rpn(["42"])                             -> 42

Follow-up questions:
- Why int(a / b) and not a // b?
- In which order do you pop the two operands?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 4.
"""


def eval_rpn(tokens: list[str]) -> int:
    raise NotImplementedError

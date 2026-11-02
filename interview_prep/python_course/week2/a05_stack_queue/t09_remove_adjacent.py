"""A5 t09 (★ optional, ~15 min). Remove adjacent duplicates.

Repeatedly remove two ADJACENT equal letters until there are none left; return the result.

Requirements:
- O(n) with a stack (not repeated string replacements).

Examples:
    remove_adjacent("abbaca")  -> "ca"     # "bb" -> "aaca" -> "aa" -> "ca"
    remove_adjacent("azxxzy")  -> "ay"
    remove_adjacent("aa")      -> ""

Follow-up questions:
- Why does a stack handle the chain reaction automatically?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t09
Теория: THEORY.md в этой папке, раздел 2.
"""


def remove_adjacent(s: str) -> str:
    raise NotImplementedError

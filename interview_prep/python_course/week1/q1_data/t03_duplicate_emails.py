"""Q1 t03 (required, ~15 min). Find duplicate emails.

Test data generators sometimes produce the same user twice. Given a list of
users {"id": int, "email": str}, return the emails that belong to more than
one user.

Requirements:
- Normalize emails before comparing: strip spaces and ignore case
  (" Ann@Mail.com " and "ann@mail.com" are the same).
- Return normalized emails (lowercase, no spaces), each once,
  in order of first appearance.

Example:
    duplicate_emails([
        {"id": 1, "email": "Ann@Mail.com"},
        {"id": 2, "email": "bob@mail.com"},
        {"id": 3, "email": " ann@mail.com "},
        {"id": 4, "email": "BOB@MAIL.COM"},
        {"id": 5, "email": "cat@mail.com"},
    ]) -> ["ann@mail.com", "bob@mail.com"]

Follow-up questions:
- Why compare with casefold() / lower() after strip()?
- Time complexity of your solution?

Run (from interview_prep/python_course/week1/q1_data): uv run pytest -k t03
Теория: interview_prep/python_course/c03_collections/s05_counter_defaultdict/THEORY.md.
"""


def duplicate_emails(users: list[dict]) -> list[str]:
    raise NotImplementedError

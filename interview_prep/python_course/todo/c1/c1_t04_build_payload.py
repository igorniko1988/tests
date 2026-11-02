"""C1 t04 (required, ~10 min). Build a request payload from a template.

Tests share one "valid order" template and override a few fields per test.
Implement build_payload(template, **changes) that returns a NEW dict:
the template with top-level keys replaced by changes.

Requirements:
- The template must never change - neither now, nor after the caller mutates
  the result (including nested dicts/lists).
- Values from changes must not be shared with the caller either.

Example:
    ORDER = {"symbol": "BTC/USDT", "side": "buy", "meta": {"tags": ["smoke"]}}

    p = build_payload(ORDER, side="sell")
    p  -> {"symbol": "BTC/USDT", "side": "sell", "meta": {"tags": ["smoke"]}}
    p["meta"]["tags"].append("x")
    ORDER["meta"]["tags"]  -> ["smoke"]        # template untouched

    tags = ["a"]
    p = build_payload({}, tags=tags)
    p["tags"].append("b")
    tags  -> ["a"]

Follow-up questions:
- Why isn't template.copy() or {**template, **changes} enough?
- What is the difference between a shallow and a deep copy?

Run (from interview_prep/python_course/todo): uv run pytest -k c1_t04
Теория: interview_prep/python_course/c01_objects/s06_copy/THEORY.md (раздел 6) и interview_prep/python_course/c01_objects/s10_autotests/THEORY.md.
"""


def build_payload(template: dict, **changes) -> dict:
    raise NotImplementedError

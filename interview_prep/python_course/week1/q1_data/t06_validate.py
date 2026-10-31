"""Q1 t06 (★ optional, ~20 min). Validate a response structure.

Without jsonschema/pydantic, check that a response has the required fields
of the required types. schema maps field name -> type, e.g.
    {"id": int, "symbol": str, "price": str, "filled": bool}

Return a list of error strings, in schema order:
- "missing: <field>" - the field is absent;
- "type: <field> expected <type>, got <type>" - wrong type
  (type names as type.__name__: int, str, bool, NoneType...).
Extra fields in data are allowed. bool is NOT a valid int here.

Examples:
    validate({"id": 1, "symbol": "BTC"}, {"id": int, "symbol": str})  -> []
    validate({"id": "1"}, {"id": int, "symbol": str})
        -> ["type: id expected int, got str", "missing: symbol"]
    validate({"id": True}, {"id": int})
        -> ["type: id expected int, got bool"]

Follow-up questions:
- Why is isinstance(True, int) True, and how do you handle it?
- type(x) is int vs isinstance(x, int): when is each right?

Run (from interview_prep/python_course/week1/q1_data): uv run pytest -k t06
Теория: interview_prep/python_course/c02_numbers_strings/s01_int/THEORY.md (bool — подкласс int, isinstance).
"""


def validate(data: dict, schema: dict[str, type]) -> list[str]:
    raise NotImplementedError

"""C9 t06 (★ optional, ~30 min). Your own Mock: record any call.

Implement a class Recorder - a tiny mock object:
- any attribute access returns a child Recorder, so chains work: r.client.orders.create;
- calling any recorder records the call in the ROOT recorder's list `calls` as
  (dotted_path, args, kwargs), e.g. ("client.get", ("/x",), {"timeout": 1});
- the root's dict `returns` sets return values by path: r.returns["client.get"] = {"id": 1};
  without a configured value a call returns None;
- `calls` and `returns` on the ROOT are real attributes (not children).
- Calling the root itself records path "" .

Example:
    r = Recorder()
    r.returns["api.get_user"] = {"id": 7}
    r.api.get_user(7)          -> {"id": 7}
    r.log.info("done")         -> None
    r.calls -> [("api.get_user", (7,), {}), ("log.info", ("done",), {})]

Follow-up questions:
- Why __getattr__ and not __getattribute__?
- What does unittest.mock.MagicMock add on top of this?

Run (from interview_prep/python_course/week3/c09_magic_methods): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 6.
"""


class Recorder:
    pass

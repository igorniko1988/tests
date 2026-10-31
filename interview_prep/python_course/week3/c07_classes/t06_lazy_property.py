"""C7 t06 (★ optional, ~25 min). Your own lazy (cached) property.

Implement a decorator class lazy_property (without functools.cached_property) used like this:

    class Report:
        def __init__(self, rows):
            self.rows = rows

        @lazy_property
        def total(self):
            return sum(self.rows)

- The method runs on the first access r.total and its result is stored per instance;
  later accesses return the stored value without calling the method.
- Different instances have different values.
- del r.total resets the cache: the next access computes again.
- Access through the class (Report.total) returns the lazy_property object itself.

Hint: implement __get__(self, instance, owner) and save the value into
instance.__dict__ under the same name - then Python finds it there first.

Follow-up questions:
- Why does writing into instance.__dict__ make later reads skip __get__?

Run (from interview_prep/python_course/week3/c07_classes): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 6.
"""


class lazy_property:
    def __init__(self, func) -> None:
        raise NotImplementedError

    def __get__(self, instance, owner):
        raise NotImplementedError

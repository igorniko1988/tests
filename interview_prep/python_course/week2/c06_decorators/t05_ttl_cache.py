"""C6 t05 (required, ~20 min). Cache with time-to-live.

Implement a decorator with parameters ttl_cache(seconds, clock=time.monotonic).
The decorated function caches its result per arguments for `seconds` seconds:
- the same arguments within `seconds` -> return the cached result, do not call;
- after `seconds` passed (now - saved_at >= seconds) -> call again and refresh the cache.

`clock` is a function returning the current time in seconds; tests pass a fake clock.
Arguments (positional and keyword) are hashable; keyword order does not matter.

Example:
    now = [0]

    @ttl_cache(seconds=10, clock=lambda: now[0])
    def get_rate(symbol):
        ...                 # expensive call

    get_rate("BTC")   # call
    get_rate("BTC")   # cached
    now[0] = 10
    get_rate("BTC")   # call again: 10 seconds passed

Follow-up questions:
- Why inject clock instead of calling time.monotonic() directly?
- Why monotonic and not time.time()?

Run (from interview_prep/python_course/week2/c06_decorators): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 4.
"""


import time
from functools import wraps  # noqa: F401


def ttl_cache(seconds: float, clock=time.monotonic):
    raise NotImplementedError

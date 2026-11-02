"""Q3 t02 (required, ~25 min). Sliding-window rate limiter.

Implement RateLimiter(limit, window, clock=time.monotonic): at most `limit` requests per any
`window` seconds (sliding window).

- allow() -> bool: True and remember the request if allowed now, otherwise False
  (rejected requests are not remembered);
- a request made at time t stops counting at time t + window (exactly);
- remaining() -> how many requests are allowed right now;
- retry_after() -> seconds until the next request will be allowed (0 if allowed now);
- limit < 1 or window <= 0 -> ValueError. Use only the injected clock.

Example (clock is a fake):
    rl = RateLimiter(2, 10, clock)      # time 0
    rl.allow(), rl.allow(), rl.allow()  -> True, True, False
    rl.retry_after()                    -> 10
    # time 10
    rl.allow()                          -> True

Follow-up questions:
- Fixed window vs sliding window: what goes wrong at the window boundary?
- How would you test the stand's "5 failed logins per 60 s -> 429"?

Run (from interview_prep/python_course/week3/q3_class_design): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 3.
"""


import time


class RateLimiter:
    def __init__(self, limit: int, window: float, clock=time.monotonic) -> None:
        raise NotImplementedError

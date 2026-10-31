import time
from collections import deque


class RateLimiter:
    def __init__(self, limit: int, window: float, clock=time.monotonic) -> None:
        if limit < 1 or window <= 0:
            raise ValueError("limit must be >= 1 and window > 0")
        self.limit = limit
        self.window = window
        self._clock = clock
        self._times = deque()

    def _drop_old(self, now: float) -> None:
        while self._times and self._times[0] + self.window <= now:
            self._times.popleft()

    def allow(self) -> bool:
        now = self._clock()
        self._drop_old(now)
        if len(self._times) < self.limit:
            self._times.append(now)
            return True
        return False

    def remaining(self) -> int:
        self._drop_old(self._clock())
        return self.limit - len(self._times)

    def retry_after(self) -> float:
        now = self._clock()
        self._drop_old(now)
        if len(self._times) < self.limit:
            return 0
        return self._times[0] + self.window - now

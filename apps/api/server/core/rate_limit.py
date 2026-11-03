"""In-process sliding-window rate limiter for the public chat endpoint.

State lives in this process only. Deploys run with `--max-instances=1`, so the
counts hold across requests; a restart resets them, which is acceptable for a
portfolio site.
"""

from __future__ import annotations

import time
from collections import OrderedDict, deque
from collections.abc import Callable


class RateLimiter:
    def __init__(
        self,
        limit: int,
        window_seconds: float,
        max_keys: int = 10_000,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.max_keys = max_keys
        self._clock = clock
        self._hits: OrderedDict[str, deque[float]] = OrderedDict()

    def allow(self, key: str) -> bool:
        """Record a hit for `key`, or return False if it is over the limit."""
        now = self._clock()
        hits = self._hits.setdefault(key, deque())
        self._hits.move_to_end(key)
        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()
        # Rotating keys (a new IP or cookie per request) must not grow memory.
        while len(self._hits) > self.max_keys:
            self._hits.popitem(last=False)
        if len(hits) >= self.limit:
            return False
        hits.append(now)
        return True

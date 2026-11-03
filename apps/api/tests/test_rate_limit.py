from server.core.rate_limit import RateLimiter


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_limit_is_per_key_and_window_slides() -> None:
    clock = _Clock()
    limiter = RateLimiter(limit=2, window_seconds=60, clock=clock)
    assert limiter.allow("a")
    assert limiter.allow("a")
    assert not limiter.allow("a")
    assert limiter.allow("b")
    clock.now = 60.0
    assert limiter.allow("a")


def test_rotating_keys_do_not_grow_memory() -> None:
    limiter = RateLimiter(limit=1, window_seconds=60, max_keys=3)
    for i in range(10):
        limiter.allow(f"key-{i}")
    assert len(limiter._hits) == 3

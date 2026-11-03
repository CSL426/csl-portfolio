from collections.abc import Iterator

import pytest
from server.routes.chat import get_chat_limits


@pytest.fixture(autouse=True)
def _fresh_chat_limits() -> Iterator[None]:
    # Limiter state is process-wide; TestClient requests all share one IP.
    get_chat_limits.cache_clear()
    yield
    get_chat_limits.cache_clear()

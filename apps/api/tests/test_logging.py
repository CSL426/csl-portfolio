import json
from collections.abc import Iterator

import pytest
import structlog
from server.core.logging import configure_logging


@pytest.fixture(autouse=True)
def _restore_logging() -> Iterator[None]:
    yield
    structlog.reset_defaults()
    configure_logging()


def test_json_logs_are_one_object_per_line_with_severity(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(json_logs=True)
    structlog.get_logger("t").warning("claude_usage", cache_read=5356, note="繁體")
    line = capsys.readouterr().out.strip().splitlines()[-1]
    record = json.loads(line)
    assert record["event"] == "claude_usage"
    assert record["severity"] == "WARNING"
    assert record["cache_read"] == 5356
    assert "繁體" in line
    assert "[" not in line


def test_terminal_logs_stay_readable_by_default(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging()
    structlog.get_logger("t").info("hello")
    out = capsys.readouterr().out
    assert "hello" in out
    with pytest.raises(json.JSONDecodeError):
        json.loads(out.strip().splitlines()[-1])


def test_unknown_app_env_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    from pydantic import ValidationError
    from server.core.config import Settings

    monkeypatch.setenv("APP_ENV", "production")
    with pytest.raises(ValidationError):
        Settings()

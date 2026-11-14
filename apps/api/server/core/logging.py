import logging
import sys
from typing import cast

import structlog
from structlog.typing import EventDict, Processor, WrappedLogger


def _add_severity(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    # Cloud Logging reads the level from `severity`; without it every line is DEFAULT.
    event_dict["severity"] = str(event_dict.pop("level", "info")).upper()
    return event_dict


def configure_logging(level: str = "INFO", json_logs: bool = False) -> None:
    """Log as one JSON object per line when `json_logs`, else for a terminal.

    Cloud Logging stores the terminal format with its colour codes as plain text,
    which makes it hard to read and impossible to filter by field.
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    renderer: list[Processor] = (
        [
            _add_severity,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(ensure_ascii=False),
        ]
        if json_logs
        else [structlog.dev.ConsoleRenderer()]
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            *renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(name))

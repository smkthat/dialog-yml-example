"""Logging configuration for the application."""

import logging

import structlog
from structlog.dev import ConsoleRenderer


def setup_logger():
    """Configure the logger.

    Sets up structlog and standard logging with console handler only.

    Returns
    -------
    structlog.stdlib.BoundLogger
        The configured structlog logger instance.

    """
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="%H:%M:%S"),
    ]

    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    console_formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processor=ConsoleRenderer(
            colors=True,
            force_colors=True,
            pad_event_to=30,
            event_key="event",
            sort_keys=False,
        ),
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)

    return structlog.get_logger()

"""Structured logging configuration for the weather service."""

import logging
import sys
from typing import Optional


def setup_logging(level: Optional[int] = None) -> logging.Logger:
    """Configure and return a structured logger for the weather service.

    Args:
        level: Logging level (defaults to INFO if not provided).

    Returns:
        Configured logger instance for the weather module.
    """
    if level is None:
        level = logging.INFO

    logger = logging.getLogger("weather")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logging()

"""Tests for the weather logging configuration."""

import logging

import pytest

from weather.logging_config import setup_logging


class TestLoggingSetup:
    """Test cases for logging configuration."""

    def test_setup_logging_returns_logger(self) -> None:
        """Test that setup_logging returns a logger instance."""
        logger = setup_logging(logging.DEBUG)
        assert isinstance(logger, logging.Logger)

    def test_setup_logging_default_level(self) -> None:
        """Test that default logging level is INFO."""
        logger = setup_logging()
        assert logger.level == logging.INFO

    def test_setup_logging_custom_level(self) -> None:
        """Test that custom logging level is applied."""
        logger = setup_logging(logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_setup_logging_handler_added_once(self) -> None:
        """Test that handlers are not duplicated on repeated calls."""
        logger1 = setup_logging()
        handler_count = len(logger1.handlers)

        logger2 = setup_logging()
        assert len(logger2.handlers) == handler_count

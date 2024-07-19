"""Pytest conftest file for fixtures and hook functions."""

from _pytest.logging import LogCaptureFixture
from loguru import logger
import pytest


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    """Enable the caplog fixture for loguru."""
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)

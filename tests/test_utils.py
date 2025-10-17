import logging
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from python_project_template.utils.utils import (
    add_file_handler,
    get_ordinal_suffix,
    get_time_elapsed_string,
    is_non_empty_file,
    kwargs_logger,
)


if TYPE_CHECKING:
    from datetime import timedelta


@pytest.mark.parametrize(
    ("file_path", "expected_output"),
    [
        ("non_existent_file", False),  # This file should not exist.
        (Path(__file__), True),  # This file itself is non-empty.
        (Path(__file__).parents[0] / "__init__.py", False),  # `__init__.py` should be empty.
    ],
)
def test_is_non_empty_file(file_path: str | Path, expected_output: bool) -> None:
    assert is_non_empty_file(file_path) == expected_output


@pytest.mark.parametrize(
    ("timestamp", "expected_output"),
    [
        (0, "0 minutes, 0 seconds"),
        (1, "0 minutes, 1 second"),
        (62, "1 minute, 2 seconds"),
        (60 * 60, "1 hour, 0 minutes, 0 seconds"),
        (60 * 60 * 24 + 123, "1 day, 0 hours, 2 minutes, 3 seconds"),
        (60 * 60 * 50 + 120, "2 days, 2 hours, 2 minutes, 0 seconds"),
    ],
)
def test_get_time_elapsed_string(timestamp: float | timedelta, expected_output: str) -> None:
    assert get_time_elapsed_string(timestamp) == expected_output


@pytest.mark.parametrize(
    ("integer", "expected_output"),
    [
        (0, "th"),
        (1, "st"),
        (2, "nd"),
        (3, "rd"),
    ]
    + [
        (-1, "st"),
        (-2, "nd"),
        (-3, "rd"),
    ]
    # All numbers between 4 and 20 have the suffix 'th'.
    + [(i, "th") for i in range(4, 21)]
    # All numbers between -20 and -4 have the suffix 'th'.
    + [(-i, "th") for i in range(4, 21)]
    + [
        (120, "th"),
        (121, "st"),
        (122, "nd"),
        (123, "rd"),
        (124, "th"),
        (-225, "th"),
        (1306, "th"),
    ],
)
def test_get_ordinal_suffix(integer: int, expected_output: str) -> None:
    assert get_ordinal_suffix(integer) == expected_output


def test_kwargs_logger(caplog: pytest.LogCaptureFixture) -> None:
    """Verify that the `kwargs_logger` decorator logs the keyword arguments passed to the decorated function."""
    caplog.set_level(logging.DEBUG)

    @kwargs_logger
    def dummy_function(**kwargs: int) -> None:
        pass

    dummy_function(keyword_argument_one=123, keyword_argument_two=321)

    assert "keyword_argument_one" in caplog.text
    assert "123" in caplog.text
    assert "keyword_argument_two" in caplog.text
    assert "321" in caplog.text


def test_add_file_handler(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)

    # Verify that the `add_file_handler` function adds a file handler to the logger.
    logger = logging.getLogger("test_logger")
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file_path = Path(temp_dir) / "test.log"
        add_file_handler(logger, log_file_path)

        message = "This message should be logged to the file."
        logger.debug(message)

        with log_file_path.open("r") as log_file:
            assert message in log_file.read()

    # If the logger already had at least one handler, the format of the file handler added by the `add_file_handler`
    # function should be the same as the format of the first handler.
    logger = logging.getLogger("test_logger")
    logger.handlers.clear()

    preexisting_handler = logging.StreamHandler()
    dummy_log_prefix = "DUMMY PREFIX"
    preexisting_handler.setFormatter(logging.Formatter(f"{dummy_log_prefix}: %(message)s"))
    logger.addHandler(preexisting_handler)

    with tempfile.TemporaryDirectory() as temp_dir:
        log_file_path = Path(temp_dir) / "test.log"
        add_file_handler(logger, log_file_path)

        message = "This message should be logged to the file."
        logger.debug(message)

        with log_file_path.open("r") as log_file:
            assert f"{dummy_log_prefix}: {message}" in log_file.read()

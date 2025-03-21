from datetime import timedelta
from pathlib import Path

import pytest

from python_project.utils.utils import get_ordinal_suffix, get_time_elapsed_string, is_non_empty_file, kwargs_logger


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
        (61, "1 minute, 1 second"),
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
        (4, "th"),
        (-205, "th"),
        (1306, "th"),
    ],
)
def test_get_ordinal_suffix(integer: int, expected_output: str) -> None:
    assert get_ordinal_suffix(integer) == expected_output


def test_kwargs_logger(caplog: pytest.LogCaptureFixture) -> None:
    """Verify that the `kwargs_logger` decorator logs the keyword arguments passed to the decorated function."""

    @kwargs_logger
    def dummy_function(**kwargs: int) -> None:
        pass

    dummy_function(keyword_argument_one=123, keyword_argument_two=321)
    assert "keyword_argument_one" in caplog.text
    assert "123" in caplog.text
    assert "keyword_argument_two" in caplog.text
    assert "321" in caplog.text

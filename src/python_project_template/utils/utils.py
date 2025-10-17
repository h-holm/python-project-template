"""Utilities."""

import enum
import logging
from datetime import timedelta
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Any

from tabulate import tabulate


if TYPE_CHECKING:
    from collections.abc import Callable


LOGGER = logging.getLogger(__name__)


class LogLevel(str, enum.Enum):
    """Log level."""

    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


def is_non_empty_file(file_path: str | Path) -> bool:
    """Return `True` if `file_path` points to a non-empty file."""
    file_path = Path(file_path)
    return file_path.is_file() and file_path.stat().st_size > 0


def get_time_elapsed_string(elapsed_time: float | timedelta) -> str:
    """Given `elapsed_time`, construct a human-readable string of how much time has elapsed."""
    td = elapsed_time if isinstance(elapsed_time, timedelta) else timedelta(seconds=elapsed_time)
    days = int(td.days)
    tot_seconds = td.seconds
    hours = int(tot_seconds / 3600)
    rest_seconds = tot_seconds % 3600
    minutes = int(rest_seconds / 60)
    seconds = int(rest_seconds % 60)

    # Decide how many units to include.
    if days:
        output_string = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    elif hours:
        output_string = f"{hours} hours, {minutes} minutes, {seconds} seconds"
    else:
        output_string = f"{minutes} minutes, {seconds} seconds"

    # Make singular if necessary.
    if days == 1:
        output_string = output_string.replace("days", "day")
    if hours == 1:
        output_string = output_string.replace("hours", "hour")
    if minutes == 1:
        output_string = output_string.replace("minutes", "minute")
    if seconds == 1:
        output_string = output_string.replace("seconds", "second")

    return output_string


def get_ordinal_suffix(integer: int) -> str:
    """Given an integer, return the correct ordinal suffix, e.g., 'st' (for 'first') if the integer is 1."""
    # All numbers ending in 10, 11, ..., 20 have the suffix 'th'.
    if 10 <= abs(integer) % 100 <= 20:  # noqa: PLR2004
        return "th"
    # All other numbers have a suffix based on the last digit.
    return {1: "st", 2: "nd", 3: "rd"}.get(abs(integer) % 10, "th")


def pretty_log_dict(arguments: dict, header: tuple[str, str] = ("key", "value")) -> None:
    """Log the keys and values of the input dictionary as a nicely-formatted table."""
    table = [list(header)]
    for k, v in arguments.items():
        table.append([k, v])
    for row in tabulate(table, headers="firstrow").splitlines():
        LOGGER.info(row)


def kwargs_logger(func: Callable) -> Callable:
    """Decorator that logs the input keyword arguments of the wrapped function."""

    @wraps(func)
    def log_kwargs(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        table = [["parameter_name", "value"]]
        for k, v in kwargs.items():
            table.append([k, v])
        for row in tabulate(table, headers="firstrow").splitlines():
            LOGGER.info(row)
        return func(*args, **kwargs)

    return log_kwargs


def add_file_handler(logger: logging.Logger, log_file_path: Path, datefmt: str = "%Y-%m-%d %H:%M:%S") -> None:
    """Add a file handler to the input `logger` in-place."""
    file_handler = logging.FileHandler(log_file_path)
    if logger.handlers and logger.handlers[0].formatter:
        # Use the same formatter as for the console output. The `._fmt` attribute of a `logging.Formatter` is pre-
        # fixed with an underscore, indicating that it is intended for private use, but given the long history and
        # widespread usage of the `logging` module, the attribute is unlikely to change. Hence, we use it here.
        formatter = logging.Formatter(logger.handlers[0].formatter._fmt, datefmt=datefmt)  # noqa: SLF001
    else:
        formatter = logging.Formatter(datefmt=datefmt)
        logger.warning("No console handler formatter was found. Using a default formatter for the file handler.")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

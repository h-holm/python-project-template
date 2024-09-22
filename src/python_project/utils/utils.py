"""Utility functions."""

import logging
from datetime import timedelta
from pathlib import Path


LOGGER = logging.getLogger(__name__)


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

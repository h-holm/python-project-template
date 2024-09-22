"""Main entrypoint of a Python application that outputs whether the specified file is non-empty."""

import logging.config
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import typer


# https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#running-a-command-line-interface-from-source-with-src-layout
if not __package__:
    # Add the grandparent directory to `sys.path` to enable running all of the following:
    # - `python path/to/this/repo/src/python_project/main.py`   from anywhere,
    # - `hatch run python src/python_project/main.py`           from the root of this repo,
    grandparent_dir = Path(__file__).parents[1]
    sys.path.insert(0, str(grandparent_dir))


from python_project.utils.utils import get_time_elapsed_string, is_non_empty_file


# Set up logging.
logging.config.fileConfig(Path(__file__).parents[0] / "logging.conf", disable_existing_loggers=False)
LOGGER = logging.getLogger()


def main(file_path: Annotated[str, typer.Argument(help="The file path to check", envvar="FILE_PATH")]) -> None:
    """Log whether the input `file_path` is a non-empty file."""
    # The timezone used for timestamps.
    tz = UTC
    start_timestamp = datetime.now(tz=tz)
    LOGGER.info(f"Script started at: {start_timestamp} ({tz}).")

    LOGGER.info(f"{is_non_empty_file(file_path)=}")

    end_timestamp = datetime.now(tz=tz)
    time_elapsed_string = get_time_elapsed_string(end_timestamp - start_timestamp)
    LOGGER.info(f"Script finished at {end_timestamp} ({tz}).")
    LOGGER.info(f"Time elapsed: {time_elapsed_string}.")


if __name__ == "__main__":
    typer.run(main)

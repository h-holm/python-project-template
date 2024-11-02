"""Main entrypoint of a Python application that outputs whether the specified file is non-empty."""

import enum
import logging.config
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import typer


# https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#running-a-command-line-interface-from-source-with-src-layout
if not __package__:  # pragma: no cover
    # Add the grandparent directory to `sys.path` to enable running all of the following:
    # - `python path/to/this/repo/src/python_project/main.py`   from anywhere,
    # - `hatch run python src/python_project/main.py`           from the root of this repo,
    sys.path.insert(0, str(Path(__file__).parents[1]))


from python_project.utils.utils import get_time_elapsed_string, is_non_empty_file


# Set up logging.
logging.config.fileConfig(Path(__file__).parents[0] / "logging.conf", disable_existing_loggers=False)
LOGGER = logging.getLogger()
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Set up the `typer` app.
app = typer.Typer()


class LogLevel(str, enum.Enum):
    """Log level."""

    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


@app.command()
def main(
    file_path: Annotated[Path, typer.Argument(help="The file path to check", envvar="FILE_PATH")],
    log_level: Annotated[LogLevel, typer.Option(help="Log level")] = LogLevel.INFO,
) -> None:
    """Log whether the input `file_path` is a non-empty file."""
    LOGGER.setLevel(log_level.upper())

    start_timestamp = datetime.now(tz=UTC)
    LOGGER.info(f"Script started at: {start_timestamp.strftime(TIMESTAMP_FORMAT)} ({UTC}).")

    LOGGER.info(f"{is_non_empty_file(file_path)=}")

    end_timestamp = datetime.now(tz=UTC)
    time_elapsed_string = get_time_elapsed_string(end_timestamp - start_timestamp)
    LOGGER.info(f"Script finished at {end_timestamp.strftime(TIMESTAMP_FORMAT)} ({UTC}).")
    LOGGER.info(f"Time elapsed: {time_elapsed_string}.")


if __name__ == "__main__":
    app()

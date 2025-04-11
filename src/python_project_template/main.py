"""Main entrypoint of a Python application that outputs the n:th number in the Fibonacci sequence."""

import functools
import logging.config
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import typer


# https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#running-a-command-line-interface-from-source-with-src-layout
if not __package__:  # pragma: no cover
    # Add the grandparent directory to `sys.path` to enable running all of the following:
    # - `python path/to/this/repo/src/python_project_template/main.py`   from anywhere,
    # - `hatch run python src/python_project_template/main.py`           from the root of this repo,
    sys.path.insert(0, str(Path(__file__).parents[1]))


from python_project_template.utils.utils import (
    LogLevel,
    add_file_handler,
    get_ordinal_suffix,
    get_time_elapsed_string,
    pretty_log_dict,
)


TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Set up the `typer` app.
app = typer.Typer()


@functools.lru_cache(None)
def fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number.

    Args:
        n (int): The position in the Fibonacci sequence.

    Returns:
        int: The nth Fibonacci number.
    """
    if n < 2:  # noqa: PLR2004
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@app.command()
def main(
    nth_number: Annotated[int, typer.Argument(help="The nth Fibonacci number to compute.", min=0, envvar="NTH_NUMBER")],
    log_level: Annotated[LogLevel, typer.Option(help="Log level")] = LogLevel.INFO,
    log_file_path: Annotated[Path | None, typer.Option(help="If provided, persist logs in this file.")] = None,
) -> None:
    """Log the `nth_number` of the Fibonacci sequence."""
    LOGGER.setLevel(log_level.upper())
    if log_file_path:
        add_file_handler(LOGGER, log_file_path, datefmt=TIMESTAMP_FORMAT)

    LOGGER.info("The following arguments and options will be used:")
    pretty_log_dict(locals(), header=("argument_name", "argument_value"))

    start_timestamp = datetime.now(tz=UTC)
    LOGGER.info(f"Script started at {start_timestamp.strftime(TIMESTAMP_FORMAT)} ({UTC})")

    LOGGER.info(f"The {nth_number}{get_ordinal_suffix(nth_number)} Fibonacci number is: {fibonacci(nth_number)}")

    end_timestamp = datetime.now(tz=UTC)
    time_elapsed_string = get_time_elapsed_string(end_timestamp - start_timestamp)
    LOGGER.info(f"Script finished at {end_timestamp.strftime(TIMESTAMP_FORMAT)} ({UTC})")
    LOGGER.info(f"Time elapsed: {time_elapsed_string}")


if __name__ == "__main__":
    # Set up logging.
    logging.config.fileConfig(
        Path(__file__).parents[0] / "logging.conf",
        {"datefmt": TIMESTAMP_FORMAT},
        disable_existing_loggers=False,
    )
    LOGGER = logging.getLogger()

    # Run the `typer` app.
    app()
else:
    # This block is executed when the module is imported. This is useful for testing purposes, as it allows us to
    # import the functions and classes defined in this file without running the `typer` app.
    LOGGER = logging.getLogger(__name__)

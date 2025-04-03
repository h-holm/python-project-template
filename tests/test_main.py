import tempfile

import pytest
from typer.testing import CliRunner

from python_project_template.main import app, fibonacci


runner = CliRunner()


@pytest.mark.parametrize(
    ("n", "nth_number"),
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (19, 4181),
        (200, 280571172992510140037611932413038677189525),
    ],
)
def test_fibonacci(n: int, nth_number: int) -> None:
    assert fibonacci(n) == nth_number


def test_main() -> None:
    # The script should succeed as long as a non-negative integer is provided.
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["100"])
    assert result.exit_code == 0

    # The script should fail if anything other than a non-negative integer is provided.
    result = runner.invoke(app, ["asd"])
    assert result.exit_code == 2

    result = runner.invoke(app, ["-1"])
    assert result.exit_code == 2

    result = runner.invoke(app, [""])
    assert result.exit_code == 2

    # The script should fail if no positional argument is passed.
    result = runner.invoke(app, [])
    assert result.exit_code == 2

    # The script should fail if an invalid log level is passed.
    result = runner.invoke(app, ["--log-level", "invalid", "1"])
    assert result.exit_code == 2

    # The script should succeed if a valid log level is passed.
    result = runner.invoke(app, ["--log-level", "debug", "1"])
    assert result.exit_code == 0

    # If a `--log-file-path` is provided, the script should output logs to that file.
    with tempfile.NamedTemporaryFile() as temp_file:
        result = runner.invoke(app, ["--log-file-path", temp_file.name, "1"])
        assert result.exit_code == 0
        assert temp_file.read()

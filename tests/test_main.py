from pathlib import Path

from typer.testing import CliRunner

from python_project.main import app


runner = CliRunner()


def test_main() -> None:
    # The script should succeed as long as a positional argument is passed.
    result = runner.invoke(app, ["--log-level", "debug", str(Path(__file__))])
    assert result.exit_code == 0

    # The script should fail if no positional argument is passed.
    result = runner.invoke(app, ["--log-level", "info"])
    assert result.exit_code == 2

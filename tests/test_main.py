from typer.testing import CliRunner

from python_project.main import app


runner = CliRunner()


def test_main() -> None:
    # The script should succeed as long as a non-negative integer is provided.
    result = runner.invoke(app, ["--log-level", "debug", "1"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["--log-level", "debug", "100"])
    assert result.exit_code == 0

    # The script should fail if anything other than a non-negative integer is provided.
    result = runner.invoke(app, ["--log-level", "info", "asd"])
    assert result.exit_code == 2

    result = runner.invoke(app, ["--log-level", "info", "-1"])
    assert result.exit_code == 2

    result = runner.invoke(app, ["--log-level", "info", ""])
    assert result.exit_code == 2

    # The script should fail if no positional argument is passed.
    result = runner.invoke(app, ["--log-level", "info"])
    assert result.exit_code == 2

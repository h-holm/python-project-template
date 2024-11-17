# Python Project Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A GitHub template repo for a containerized Python application.

## Features ✅

* Seamless environment management via [Hatch](https://hatch.pypa.io/latest)
* Lightning-fast dependency resolution via [uv](https://github.com/astral-sh/uv)
* Primary dependencies and tooling configuration in the [PEP](https://peps.python.org/pep-0621)-recommended [pyproject.toml](./pyproject.toml) file
* (Sub-)dependency locking in `requirements.txt` files via [hatch-pip-compile](https://github.com/juftin/hatch-pip-compile)
* Linting and formatting using [ruff](https://github.com/astral-sh/ruff)
* Static type checking using [mypy](https://github.com/python/mypy)
* [pytest](https://docs.pytest.org) for unit tests with [coverage](https://coverage.readthedocs.io/en/7.6.7)-based reporting
* Automatic set up of [pre-commit](https://github.com/pre-commit/pre-commit) hooks via the `lint` Hatch environment
* [./src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout) to separate application logic from tests and project metadata
* Sane logging configured in a single [logging.conf](./src/python_project/logging.conf) file
* Optional quality-of-life add-ons:
  * (further) enforcing of uniform formatting via an [.editorconfig](./.editorconfig)
  * recommended [VS Code](https://code.visualstudio.com) settings and extensions through a [.vscode](./.vscode) subdirectory
  * a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers)-based development environment

The repository contains an example [GitHub Actions](./.github/workflows/) CI pipeline that:

* runs [ruff](https://github.com/astral-sh/ruff)-based linting and formatting, [mypy](https://github.com/python/mypy)-based static type checking, [pytest](https://docs.pytest.org)-based unit testing,
* performs a [CodeQL](https://codeql.github.com) vulnerability scan,
* builds and pushes a well-labeled container image to [Google Cloud Artifact Registry](https://cloud.google.com/artifact-registry/docs),
* executes a simple integration test on [Google Cloud Run](https://cloud.google.com/run?hl=en).

## Requirements

Ensure [Hatch](https://hatch.pypa.io/latest) is [installed](https://hatch.pypa.io/latest/install) on your system.

## Development

### Running the Code

Run the [main.py](./src/python_project/main.py) entrypoint with the `--help` flag for an explanation to the application logic:

```shell
hatch run python src/python_project/main.py --help          # Uses the "default" Hatch environment.
hatch run default:python src/python_project/main.py --help  # Equivalent to not specifying "default:".
```

### Unit Tests

Run the `test` script of the "test" Hatch environment to execute the [`pytest`](https://docs.pytest.org/en/stable)-backed unit tests and generate a [coverage](https://coverage.readthedocs.io/en/7.6.7) report:

```shell
hatch run test:test
```

### Formatting, Linting and Type Checking

Run the `lint` script of the "lint" Hatch environment to perform (1) formatting and linting using [`ruff`](https://github.com/astral-sh/ruff) and (2) static type checking using [`mypy`](https://github.com/python/mypy).

```shell
hatch run lint:lint
```

### Bumping the Version

Run `hatch version` followed by the [SemVer](https://semver.org) component to bump, e.g.:

```shell
hatch version patch  # Or `hatch version minor` or `hatch version major`.
```

Commit the updated [\_\_version\_\_.py](./src/python_project/__version__.py) script to version control before creating a `git` tag. Ensure the tag has the same name as the (now bumped) version:

```shell
git tag -a $(hatch version) -m 'Descriptive tag message'
```

## License

See [LICENSE](LICENSE).

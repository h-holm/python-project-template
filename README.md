# Python Project Template

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://docs.python.org/3/whatsnew/3.14.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-9400d3.svg)](https://opensource.org/licenses/MIT)
[![Hatch](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/type%20checked-mypy-039dfc)](https://github.com/python/mypy)
[![Pytest](https://img.shields.io/static/v1?label=‎&message=Pytest&logo=Pytest&color=b647c4&logoColor=white)](https://docs.pytest.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Deploy to Cloud Run](https://github.com/h-holm/python-project-template/workflows/Deploy%20to%20Cloud%20Run/badge.svg)](https://github.com/h-holm/python-project-template/actions/workflows/deploy-to-cloud-run.yaml)
[![CodeQL](https://github.com/h-holm/python-project-template/workflows/CodeQL%20Analysis/badge.svg)](https://github.com/h-holm/python-project-template/actions/workflows/codeql-analysis.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/h-holm/python-project-template/main.svg)](https://results.pre-commit.ci/latest/github/h-holm/python-project-template/main)

A template repo that enables quickly setting up an end-to-end CI/CD pipeline that tests and deploys a containerized
Python application. The placeholder Python logic computes a Fibonacci number.

## Features ✅

* Seamless environment management via [Hatch](https://hatch.pypa.io/latest)
* Lightning-fast dependency resolution via [uv](https://github.com/astral-sh/uv)
* Primary dependencies and tooling configuration in the [PEP](https://peps.python.org/pep-0621)-recommended
[pyproject.toml](./pyproject.toml) file
* (Sub-)dependency locking in `requirements.txt` files via
[hatch-pip-compile](https://github.com/juftin/hatch-pip-compile)
* Linting and formatting using [ruff](https://github.com/astral-sh/ruff)
* Static type checking using [mypy](https://github.com/python/mypy)
* [pytest](https://docs.pytest.org) for unit tests with [coverage](https://coverage.readthedocs.io/en/7.6.7)-based
reporting
* [./src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout) to separate application
logic from tests and project metadata
* Sane logging configured in a single [logging.conf](./src/python_project_template/logging.conf) file
* Optional quality-of-life add-ons:
  * [pre-commit](https://github.com/pre-commit/pre-commit) hooks installable via the `hooks` script of the `lint` Hatch
  environment
  * (further) enforcing of uniform formatting via an [.editorconfig](./.editorconfig)
  * recommended [VS Code](https://code.visualstudio.com) settings and extensions through a [.vscode](./.vscode)
  subdirectory
  * a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers)-based development environment

### [GitHub Actions](./.github/workflows/) [CI/CD](https://www.redhat.com/en/topics/devops/what-is-ci-cd)

On any pull request, target a `stg` staging environment and:

* run [ruff](https://github.com/astral-sh/ruff)-based linting and formatting,
[mypy](https://github.com/python/mypy)-based static type checking, and [pytest](https://docs.pytest.org)-based unit
testing;
* perform a [CodeQL](https://codeql.github.com) vulnerability scan;
* build and push a well-labeled container image to a
[Google Cloud Artifact Registry](https://cloud.google.com/artifact-registry/docs);
* execute an integration test on [Google Cloud Run](https://cloud.google.com/run?hl=en) that runs the application
logic end-to-end.

On a commit/tag being merged/pushed (in)to the `main` branch, target a `prd` production environment and:

* perform the same steps as above;
* deploy a Cloud Run job;
* promote the now-vetted container image by adding tags such as `latest`, `main` and the [SemVer](https://semver.org)
tag (if any).

## Requirements

Ensure [Hatch](https://hatch.pypa.io/latest) is [installed](https://hatch.pypa.io/latest/install) on your system. With
Hatch installed, there is no need to manually create environments and install dependencies; that is all handled by
Hatch.

## Development

### Running the Code

Run the [main.py](./src/python_project_template/main.py) entrypoint with the `--help` flag for an explanation to the
application logic:

```shell
hatch run python src/python_project_template/main.py --help          # Uses the "default" Hatch environment.
hatch run default:python src/python_project_template/main.py --help  # Equivalent to not specifying "default:".
```

### Unit Testing

The `test` Hatch environment defines [scripts](https://hatch.pypa.io/1.13/how-to/run/python-scripts) that can be used
to execute and debug the [`pytest`](https://docs.pytest.org/en/stable)-backed unit tests and generate a
[coverage](https://coverage.readthedocs.io/en/7.6.7) report:

```shell
hatch run test:test                      # To run all unit tests under the `./tests` subdirectory.
hatch run test:test tests/test_utils.py  # To execute the `tests/test_utils.py` unit tests.
hatch run test:debug                     # To perform unit testing in `pytest` debug mode.
hatch run test:cov-xml                   # To generate a `coverage.xml` that can be consumed by code scanners.
```

### Formatting, Linting and Type Checking

The `lint` Hatch environment defines scripts to (1) perform [`ruff`](https://github.com/astral-sh/ruff)-based
formatting and linting, (2) run [`mypy`](https://github.com/python/mypy)-based static type checking and (3) set up
[`pre-commit`](https://github.com/pre-commit/pre-commit) hooks synced with the environment:

```shell
hatch run lint:lint    # To run a `ruff`-based style check followed by `mypy` type checking.
hatch run lint:style   # To run (only) a `ruff`-based style check.
hatch run lint:typing  # To run (only) `mypy`-based type checking.
hatch run lint:fix     # To attempt to fix issues identified by `ruff`.
hatch run lint:hooks   # To set up `pre-commit` hooks that always align with the "lint" Hatch environment.
```

### Upgrading Dependencies

```shell
hatch run upgrade-all                          # To upgrade all Python dependencies of the `default` Hatch environment.
hatch run upgrade-pkg $PACKAGE_NAME            # To upgrade $PACKAGE_NAME in the `default` Hatch environment.
hatch run $ENV_NAME:upgrade-all                # To upgrade all Python dependencies in the specified Hatch environment.
hatch run $ENV_NAME:upgrade-pkg $PACKAGE_NAME  # To upgrade $PACKAGE_NAME in the specified Hatch environment.
```

### Bumping the Version

Run `hatch version` followed by the [SemVer](https://semver.org) component to bump, e.g.:

```shell
hatch version patch  # Or `hatch version minor` or `hatch version major`.
```

Commit the updated [\_\_version\_\_.py](./src/python_project_template/__version__.py) script to version control before
creating a `git` tag. Ensure the tag has the same name as the (now bumped) version:

```shell
git tag -a $(hatch version) -m 'Descriptive tag message'
```

## License

See [LICENSE](LICENSE).

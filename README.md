# Python Project Template

A GitHub template repo for a containerized Python application.

* [Hatch](https://hatch.pypa.io/latest) is used to manage the development environments and production build.
* Primary dependencies and configurations are handled in the [pyproject.toml](./pyproject.toml) file.
* All (sub-)dependencies are locked via `requirements.txt` files using [`hatch-pip-compile`](https://github.com/juftin/hatch-pip-compile).
* Hatch is configured to automatically set up [`pre-commit` hooks](https://github.com/pre-commit/pre-commit) that are synced with the `lint` Hatch environment.
* The application logic is defined under [src/python_project](src/python_project).
* Logging is configured in a single [logging.conf](./src/python_project/logging.conf) file.
* Optionally, uniform formatting can further be ensured via the [.editorconfig](./.editorconfig) and [.vscode](./.vscode) configs.

The repository contains an example [GitHub Actions CI pipeline](./.github/workflows/) that:

* runs [`ruff`](https://github.com/astral-sh/ruff)-based linting and formatting,
* runs [`mypy`](https://github.com/python/mypy)-based static type checking,
* runs [`pytest`](https://docs.pytest.org)-based unit testing,
* performs a CodeQL vulnerability scan,
* builds and pushes a well-labeled container image to [Google Cloud Artifact Registry](https://cloud.google.com/artifact-registry/docs),
* executes a simple integration test on [Google Cloud Run](https://cloud.google.com/run?hl=en).

## Requirements

Ensure [Hatch](https://hatch.pypa.io/latest) is [installed](https://hatch.pypa.io/latest/install) on your system.

## Development

### Running the Code

Run the [main.py](./src/python_project/main.py) entrypoint via the default Hatch environment with the `--help` flag for an explanation to the application logic:

```shell
hatch run python src/python_project/main.py --help
```

```shell
hatch run default:python src/python_project/main.py --help  # Equivalent to not specifying "default:".
```

### Unit Tests

Run the `test` script of the "test" Hatch environment to execute the unit tests and generate a coverage report using [`pytest`](https://docs.pytest.org/en/stable).

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

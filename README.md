# Python Project Template

A GitHub template repo for a containerized Python application.

## Requirements

[Hatch](https://hatch.pypa.io/latest) is used to manage the development environment and production build. Ensure it is [installed](https://hatch.pypa.io/latest/install) on your system.

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

Run the `all` script of the "lint" Hatch environment to perform (1) formatting and linting using [`ruff`](https://github.com/astral-sh/ruff) and (2) static type checking using [`mypy`](https://github.com/python/mypy).

```shell
hatch run lint:all
```

### Publish a New Version

Run either of the following commands to bump the version and create a commit and associated tag:

```shell
hatch version patch
```

```shell
hatch version minor
```

```shell
hatch version major
```

Your default Git text editor will open so you can add information about the release.

## License

See [LICENSE](LICENSE).

# Contributing

Pull requests are welcome and appreciated. For major changes, please open an
issue first to discuss what you would like to change. If you have found a bug or
have a feature request, please open an issue.

## Development

Tabbit is written in Python. You will need to install [uv], which is used to
manage the project.

Optionally, you can use [pre-commit] to install pre-commit hooks that run checks
whilst making a commit.

```shell
uv tool install pre-commit
pre-commit install
```

When sending a patch, ensure your code passes checks and the test suite.

```shell
uv run --frozen pytest
uv run --frozen mypy src tests
uvx pre-commit run --all-files
```

These checks are run via GitHub Actions and will block merging if any fail.
Running them locally saves time and expedites the review process.

### Testing

If you are adding a new feature, test the feature works as expected. If you are
fixing an issue, add a test that fails on the receiving branch and passes on the
merging branch.

### Typing

All code must pass `mypy` checks. Avoid using `# type: ignore`, `typing.Any`,
and `typing.cast` (which undermine the type system) unless due to a bug with the
type-checker or a limitation of Python's type system.

## Project structure

Application code is stored in the `tabbit` directory in `src`. For new
contributors, the following top-level overview may be helpful.

- `tabbit.config`: manages configuration (such as application settings and
  logging).
- `tabbit.database`: manages database operations (such as creating, reading,
  updating, and deleting data), models for representing database objections, and
  session management.
- `tabbit.routers`: manages the user-facing API.
- `tabbit.schemas`: describes and manages the intermediary data between the API
  and database.
- `tabbit.asgi`: manages the ASGI application.

[uv]: https://docs.astral.sh/uv/
[pre-commit]: https://pre-commit.com/

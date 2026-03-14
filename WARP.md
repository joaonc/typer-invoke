# typer-invoke Project Rules

## Package Management

Use `uv` for all package management. Do **not** use `pip` directly.

```bash
# Install packages
uv pip install <package>

# Install from requirements file
uv pip install -r admin/requirements/requirements-dev.txt

# Compile requirements
uv pip compile admin/requirements/requirements-dev.in -o admin/requirements/requirements-dev.txt
```

## Development Setup

[`uv`](https://docs.astral.sh/uv/) is required. Install it first, then set up the environment:

```bash
uv venv
uv pip install -r admin/requirements/requirements-dev.txt
```

## Linting and Formatting

Use `ruff` (not `black`, `isort`, or `flake8`):

```bash
# Fix issues and format
ruff check --fix .
ruff format .

# Check only (CI mode)
ruff check .
ruff format --check .
```

## Building and Publishing

Use `uv build` and `uv publish` (not `flit`):

```bash
uv build
uv publish
```

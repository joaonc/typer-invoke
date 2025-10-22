import importlib
import sys

import typer


def load_module_app(module_path: str) -> typer.Typer | None:
    """Load a Typer app from a module path like 'sample.hello'."""
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, 'app') and isinstance(module.app, typer.Typer):
            return module.app
        else:
            typer.echo(
                f'Warning: Module `{module_path}` does not have a Typer app instance named `app`',
                err=True,
            )
            return None
    except ImportError as e:
        typer.echo(f'Error: Could not import module `{module_path}`: {e}', err=True)
        return None


def create_app(module_paths: list[str]) -> typer.Typer:
    """Create a main Typer app with subcommands from specified modules."""
    app = typer.Typer()

    for module_path in module_paths:
        # Extract the module name (last part of the path) to use as subcommand name
        module_name = module_path.split('.')[-1]

        # Load the module's Typer app
        module_app = load_module_app(module_path)

        if module_app:
            # Add the module's app as a subcommand group
            app.add_typer(module_app, name=module_name)

    return app


def main(module_paths: list[str] | None = None):
    """Entry point for the invoke CLI.

    Args:
        module_paths: List of module paths to load. If None, reads from sys.argv.
    """
    if module_paths is None:
        # Parse command line arguments
        # sys.argv[0] is the script name, we need at least one module path
        if len(sys.argv) < 2:
            typer.echo('Error: No module paths specified', err=True)
            typer.echo('Usage: python -m src <module_path> [command] [args...]', err=True)
            typer.echo('Example: python -m src sample.hello world', err=True)
            sys.exit(1)

        # First argument is the module path, rest are passed to the app
        module_paths = [sys.argv[1]]
        # Remove the module path from sys.argv so Typer gets the remaining args
        sys.argv = [sys.argv[0]] + sys.argv[2:]

    app = create_app(module_paths)
    app()


if __name__ == '__main__':
    main()

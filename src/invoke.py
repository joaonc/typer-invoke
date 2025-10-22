import importlib
import sys
from pathlib import Path

import typer


def load_module_app(module_path: str) -> typer.Typer | None:
    """Load a Typer app from a module path like 'sample.hello'."""
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, 'app') and isinstance(module.app, typer.Typer):
            return module.app
        else:
            typer.echo(
                f"Warning: Module '{module_path}' does not have a Typer app instance named 'app'",
                err=True,
            )
            return None
    except ImportError as e:
        typer.echo(f"Error: Could not import module '{module_path}': {e}", err=True)
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


def main():
    """Entry point for the invoke CLI."""
    # For now, hardcode the modules to load (can be made configurable later)
    module_paths = ['sample.hello']

    app = create_app(module_paths)
    app()


if __name__ == '__main__':
    main()

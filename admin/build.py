import typer

from . import PROJECT_ROOT

app = typer.Typer()

BUILD_DIST_DIR = PROJECT_ROOT / 'dist'


@app.command()
def clean():
    import shutil

    shutil.rmtree(BUILD_DIST_DIR, ignore_errors=True)


if __name__ == '__main__':
    app()

import pytest
from rich.console import Console

from src.logging_rich import get_logger


@pytest.fixture(scope='session')
def console():
    return Console(stderr=True, force_terminal=True)


@pytest.fixture(scope='session')
def logger():
    return get_logger()

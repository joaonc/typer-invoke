"""
Comprehensive example of Python logging with Rich package for enhanced console output.
This example demonstrates custom formatting, different log levels, and Rich markup usage.
"""

import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.highlighter import ReprHighlighter
from rich.traceback import install

# Install rich traceback handler for better error display
install(show_locals=True)

# Create a custom console instance for more control
console = Console(stderr=True, force_terminal=True)


class CustomRichHandler(RichHandler):
    """
    Custom Rich handler that provides different formatting for each log level.

    This extends ``RichHandler`` to customize the appearance of different log levels.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            console=console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            **kwargs
        )

    def emit(self, record):
        """
        Custom emit method to handle different log level formatting.
        """
        # Store original message
        msg = record.getMessage()

        # Apply custom formatting based on log level
        if record.levelno >= logging.ERROR:
            record.msg = f'[bold red]ERROR:[/bold red] [red]{msg}[/red]'
        elif record.levelno >= logging.WARNING:
            record.msg = f'[yellow]{msg}[/yellow]'
        elif record.levelno >= logging.INFO:
            record.msg = msg
        elif record.levelno >= logging.DEBUG:
            record.msg = f'[dim]{msg}[/dim]'

        super().emit(record)


def setup_logging(log_level=logging.DEBUG) -> logging.Logger:
    """
    Set up logging configuration with Rich handler and custom formatting.

    :param log_level: The minimum log level to display (default: DEBUG)
    :returns: Configured logger instance.
    """

    # Create logger
    logger = logging.getLogger('rich_example')
    logger.setLevel(log_level)
    logger.handlers.clear()
    rich_handler = CustomRichHandler(
        level=log_level,
        show_time=True,
        show_level=True,
        show_path=True,
        enable_link_path=True,
        highlighter=ReprHighlighter(),
    )

    # Set custom format string and add handler
    formatter = logging.Formatter(
        fmt='%(message)s',
        datefmt='[%X]'  # Time format: [HH:MM:SS]
    )
    rich_handler.setFormatter(formatter)
    logger.addHandler(rich_handler)

    # Prevent logs from being handled by root logger (avoid duplicate output)
    logger.propagate = False

    return logger

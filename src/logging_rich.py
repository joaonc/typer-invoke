"""
Comprehensive example of Python logging with Rich package for enhanced console output.
This example demonstrates custom formatting, different log levels, and Rich markup usage.
"""

import logging
import sys
from datetime import datetime
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
            record.msg = f"[bold red]ERROR:[/bold red] [red]{msg}[/red]"
        elif record.levelno >= logging.WARNING:
            record.msg = f"[yellow]{msg}[/yellow]"
        elif record.levelno >= logging.INFO:
            record.msg = msg
        elif record.levelno >= logging.DEBUG:
            record.msg = f"[dim]{msg}[/dim]"

        super().emit(record)


def setup_logging(log_level=logging.DEBUG):
    """
    Set up logging configuration with Rich handler and custom formatting.

    Args:
        log_level: The minimum log level to display (default: DEBUG)

    Returns:
        logging.Logger: Configured logger instance
    """

    # Create logger
    logger = logging.getLogger("rich_example")
    logger.setLevel(log_level)

    # Clear any existing handlers to avoid duplicate logs
    logger.handlers.clear()

    # Create and configure Rich handler
    rich_handler = CustomRichHandler(
        level=log_level,
        show_time=True,  # Show timestamps
        show_level=True,  # Show log level
        show_path=True,  # Show file path
        enable_link_path=True,  # Make paths clickable in supported terminals
        highlighter=ReprHighlighter(),  # Syntax highlighting for repr() output
    )

    # Set custom format string
    # This controls what information is displayed and in what order
    formatter = logging.Formatter(
        fmt="%(message)s",  # We handle the formatting in our custom handler
        datefmt="[%X]"  # Time format: [HH:MM:SS]
    )
    rich_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(rich_handler)

    # Prevent logs from being handled by root logger (avoid duplicate output)
    logger.propagate = False

    return logger

def main():
    """
    Main function to demonstrate the Rich logging setup and usage.
    """

    # Print welcome message
    console.print("[bold green]Python Logging with Rich - Comprehensive Example[/bold green]")
    console.print(
        "[dim]This example demonstrates custom formatting, log levels, and Rich markup[/dim]\n")

    # Set up logging with DEBUG level (shows all messages)
    logger = setup_logging(log_level=logging.DEBUG)

    # Log application start
    logger.info("🚀 [bold]Application started[/bold] - Rich logging configured")

    # Run demonstrations
    demonstrate_log_levels(logger)
    demonstrate_rich_markup(logger)
    demonstrate_structured_logging(logger)
    demonstrate_error_handling(logger)

    # Log application end
    logger.info("✅ [bold green]All demonstrations completed successfully[/bold green]")

    # Show example of changing log level at runtime
    console.print("\n[bold blue]📝 Changing Log Level to INFO (hiding DEBUG messages)[/bold blue]")
    console.print("=" * 60)

    logger.setLevel(logging.INFO)
    logger.debug("This debug message will NOT be shown")
    logger.info("This info message WILL be shown")
    logger.warning("Log level changed - debug messages are now hidden")


if __name__ == "__main__":
    # Run the main demonstration
    main()

    # Additional notes
    console.print(f"\n[bold blue]📚 Additional Notes:[/bold blue]")
    console.print("• Rich markup can be used in any log message")
    console.print("• Tracebacks are automatically formatted with Rich")
    console.print("• Log levels can be changed at runtime")
    console.print("• File paths in logs are clickable in supported terminals")
    console.print("• This configuration is production-ready and can be adapted for your needs")
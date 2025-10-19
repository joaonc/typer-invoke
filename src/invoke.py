import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Import the appropriate TOML library
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError(
            "tomli is required for Python < 3.11. Install with: pip install tomli"
        )


def find_pyproject_toml(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Find pyproject.toml by walking up the directory tree from start_path.

    :param start_path: Directory to start searching from. Defaults to current working directory.
    :type start_path: Optional[Path]
    :returns: Path to pyproject.toml if found, None otherwise.
    :rtype: Optional[Path]
    """
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path).resolve()

    # Walk up the directory tree.
    for parent in [current] + list(current.parents):
        pyproject_path = parent / "pyproject.toml"
        if pyproject_path.exists():
            return pyproject_path

    return None


def read_invoke_config(pyproject_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Read invoke configuration from pyproject.toml.

    :param pyproject_path: Path to pyproject.toml. If None, searches for it automatically.
    :type pyproject_path: Optional[Path]
    :returns: Dictionary containing invoke configuration, empty dict if not found.
    :rtype: Dict[str, Any]
    :raises FileNotFoundError: If pyproject.toml is not found
    :raises tomllib.TOMLDecodeError: If pyproject.toml is malformed
    """
    if pyproject_path is None:
        pyproject_path = find_pyproject_toml()

    if pyproject_path is None:
        raise FileNotFoundError(
            "pyproject.toml not found in current directory or any parent directory")

    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        # Extract invoke-specific configuration.
        return data.get("tool", {}).get("invoke", {})

    except Exception as e:
        raise Exception(f"Error reading {pyproject_path}: {e}")


def get_invoke_setting(key: str, default: Any = None, pyproject_path: Optional[Path] = None) -> Any:
    """
    Get a specific invoke setting from pyproject.toml.

    :param key: Configuration key to retrieve
    :type key: str
    :param default: Default value if key is not found
    :type default: Any
    :param pyproject_path: Path to pyproject.toml
    :type pyproject_path: Optional[Path]
    :returns: The configuration value or default
    :rtype: Any
    """
    try:
        config = read_invoke_config(pyproject_path)
        return config.get(key, default)
    except (FileNotFoundError, Exception):
        return default


# Example usage and utility class
class InvokeConfig:
    """
    Configuration manager for invoke settings from ``pyproject.toml``.
    """

    def __init__(self, pyproject_path: Optional[Path] = None):
        """
        Initialize InvokeConfig.

        :param pyproject_path: Path to pyproject.toml
        :type pyproject_path: Optional[Path]
        """
        self.pyproject_path = pyproject_path
        self._config = None

    @property
    def config(self) -> Dict[str, Any]:
        """
        Lazy-load configuration.

        :returns: Dictionary containing invoke configuration
        :rtype: Dict[str, Any]
        """
        if self._config is None:
            try:
                self._config = read_invoke_config(self.pyproject_path)
            except (FileNotFoundError, Exception):
                self._config = {}
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        :param key: Configuration key to retrieve
        :type key: str
        :param default: Default value if key is not found
        :type default: Any
        :returns: The configuration value or default
        :rtype: Any
        """
        return self.config.get(key, default)

    def reload(self) -> None:
        """
        Reload configuration from file.
        """
        self._config = None


# Example usage
if __name__ == "__main__":
    # Method 1: Direct function calls
    try:
        config = read_invoke_config()
        print("Invoke configuration:", config)

        # Get specific settings
        task_timeout = get_invoke_setting("task_timeout", default=300)
        debug_mode = get_invoke_setting("debug", default=False)

        print(f"Task timeout: {task_timeout}")
        print(f"Debug mode: {debug_mode}")

    except FileNotFoundError:
        print("No pyproject.toml found")
    except Exception as e:
        print(f"Error: {e}")

    # Method 2: Using the config class
    invoke_config = InvokeConfig()
    task_timeout = invoke_config.get("task_timeout", 300)
    custom_tasks_dir = invoke_config.get("tasks_dir", "tasks")

    print(f"Using config class - timeout: {task_timeout}, tasks_dir: {custom_tasks_dir}")

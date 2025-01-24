import importlib.metadata
import toml
from pathlib import Path

# poetry version [command]:

# patch: Increments the patch version.
# Example: 1.0.0 to 1.0.1.

# minor: Increments the minor version.
# Example: 1.0.0 to 1.1.0.

# major: Increments the major version.
# Example: 1.0.0 to 2.0.0.


def get_version() -> str:
    try:
        # Try to get the version from the installed package metadata
        return importlib.metadata.version("rsna-anonymizer")
    except importlib.metadata.PackageNotFoundError:
        # Fallback to reading the version from pyproject.toml
        pyproject_path = Path(__file__).resolve().parent.parent.parent.parent / "pyproject.toml"
        if not pyproject_path.exists():
            raise FileNotFoundError("pyproject.toml not found")
        pyproject_data = toml.load(pyproject_path)
        return pyproject_data["tool"]["poetry"]["version"]

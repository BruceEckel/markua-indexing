from pathlib import Path

project_dir = Path(__file__).parent.parent.parent


class TopDir:
    """
    Directory off of the project root that is guaranteed to exist.
    """

    def __init__(self, subdir_name: str, project_directory: Path = project_dir):
        self.directory: Path = project_directory / subdir_name
        self.directory.mkdir(parents=True, exist_ok=True)

    def __truediv__(self, other: str) -> Path:
        """Used with '/' to specify files within the directory."""
        return self.directory / other

    def __str__(self) -> str:
        """String representation of the directory path."""
        return str(self.directory)

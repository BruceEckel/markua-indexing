"""
Unless an exception occurs, automatically delete the file when the ScopedFile object goes out of scope.
Python's __del__() method handles normal cleanup and a context manager handles exceptions.
The __del__() method is automatically called when the object is garbage collected
(typically when it goes out of scope), and it will delete the file only if the object leaves
the scope without encountering an exception.
"""
from pathlib import Path


class ScopedFile:
    def __init__(self, file_name: str, dir_path: Path = Path()):
        self.file_name = file_name
        self.dir_path = dir_path  # Defaults to current directory
        self.file_path = self.dir_path / self.file_name
        self.file_path.write_text('', encoding='utf-8')
        # Track whether the scope exits normally
        self._normal_exit = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # If an exception occurred, set _abnormal_exit to True
        if exc_type is not None:
            self._normal_exit = False
        # Return False to propagate exceptions
        return False

    def __del__(self):
        # Delete the file if we exit the scope without an exception
        if self._normal_exit and self.file_path.exists():
            try:
                self.file_path.unlink()
            except Exception as e:
                print(f"Failed to delete {self.file_path}: {e}")

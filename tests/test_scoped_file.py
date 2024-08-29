import pytest
from pathlib import Path
from markua_indexing.scoped_file import ScopedFile 


@pytest.fixture
def temp_dir(tmp_path):
    # Create a temporary directory
    return tmp_path


def test_normal_exit_deletes_file(temp_dir):
    # Ensure the file is created in the specified directory
    file_name = "test_scoped_file.txt"
    with ScopedFile(file_name, temp_dir) as scoped_file:
        assert scoped_file.file_path.exists()
    # Explicitly delete the scoped_file object to trigger __del__
    del scoped_file
    # After the scope ends and object is deleted, the file should be deleted
    assert not (temp_dir / file_name).exists()


def test_exception_leaves_file(temp_dir):
    file_name = "test_scoped_file.txt"
    try:
        with ScopedFile(file_name, temp_dir) as scoped_file:
            assert scoped_file.file_path.exists()
            # Simulate an exception
            raise Exception("Test exception")
    except Exception:
        pass
    del scoped_file
    assert (temp_dir / file_name).exists()


def test_manual_delete(temp_dir):
    # Manually delete the file inside the block
    file_name = "test_scoped_file.txt"
    with ScopedFile(file_name, temp_dir) as scoped_file:
        assert scoped_file.file_path.exists()
        scoped_file.file_path.unlink()  
        assert not scoped_file.file_path.exists()  # Check that it's deleted during the block
    # The file should not be recreated after the block ends
    assert not (temp_dir / file_name).exists()


def test_no_file_on_instantiation(temp_dir):
    # Ensure the file does not exist before instantiation
    file_name = "test_scoped_file.txt"
    file_path = temp_dir / file_name
    assert not file_path.exists()
    with ScopedFile(file_name, temp_dir) as scoped_file:
        assert scoped_file.file_path.exists()
    del scoped_file
    assert not file_path.exists()


def test_default_directory(temp_dir):
    # Test that the file is created in the current directory by default
    file_name = "test_scoped_file.txt"
    with ScopedFile(file_name) as scoped_file:
        assert scoped_file.file_path.exists()
        assert scoped_file.file_path.parent == Path()
    del scoped_file
    assert not Path(file_name).exists()

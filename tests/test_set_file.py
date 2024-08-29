import pytest
from markua_indexing.scoped_file import SetFile


@pytest.fixture
def temp_dir(tmp_path):
    # Create a temporary directory using pytest's tmp_path fixture
    return tmp_path


def test_add_item_to_set(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        set_file.add("apple")
        set_file.add("banana")

        # Check if the file exists and contains the correct items
        expected_content = "apple\nbanana\n"
        assert set_file.file_path.exists()
        assert set_file.file_path.read_text(encoding='utf-8') == expected_content


def test_remove_item_from_set(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        set_file.add("apple")
        set_file.add("banana")
        set_file.remove("apple")

        # Check if the file exists and contains only "banana"
        expected_content = "banana\n"
        assert set_file.file_path.exists()
        assert set_file.file_path.read_text(encoding='utf-8') == expected_content


def test_no_duplicate_items(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        set_file.add("apple")
        set_file.add("apple")
        set_file.add("banana")

        # Check if the file contains only unique items
        expected_content = "apple\nbanana\n"
        assert set_file.file_path.exists()
        assert set_file.file_path.read_text(encoding='utf-8') == expected_content


def test_file_deletion_on_normal_exit(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        set_file.add("apple")
        set_file.add("banana")

    # After the scope ends, the file should be deleted
    del set_file
    assert not (temp_dir / file_name).exists()


def test_file_persistence_on_exception(temp_dir):
    file_name = "test_set_file.txt"

    try:
        with SetFile(file_name, temp_dir) as set_file:
            set_file.add("apple")
            set_file.add("banana")
            raise Exception("Test exception")
    except Exception:
        pass

    # After an exception, the file should still exist and contain the correct data
    expected_content = "apple\nbanana\n"
    assert (temp_dir / file_name).exists()
    assert (temp_dir / file_name).read_text(encoding='utf-8') == expected_content


def test_remove_nonexistent_item(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        set_file.add("apple")
        set_file.remove("banana")  # Attempt to remove an item not in the set

        # The file should still contain only "apple"
        expected_content = "apple\n"
        assert set_file.file_path.exists()
        assert set_file.file_path.read_text(encoding='utf-8') == expected_content


def test_add_collection_with_list(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        set_file.add_collection(["apple", "banana", "cherry"])

        # Check if the file exists and contains the correct items
        expected_content = "apple\nbanana\ncherry\n"
        assert set_file.file_path.exists()
        assert set_file.file_path.read_text(encoding='utf-8') == expected_content


def test_add_collection_with_set(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        set_file.add_collection({"date", "elderberry", "fig"})

        # Check if the file exists and contains the correct items
        expected_content = "date\nelderberry\nfig\n"
        assert set_file.file_path.exists()
        assert set_file.file_path.read_text(encoding='utf-8') == expected_content


def test_add_collection_mixed_with_existing_items(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        set_file.add("apple")
        set_file.add_collection(["banana", "cherry"])
        set_file.add_collection({"date", "elderberry"})

        # Check if the file exists and contains all the items
        expected_content = "apple\nbanana\ncherry\ndate\nelderberry\n"
        assert set_file.file_path.exists()
        assert set_file.file_path.read_text(encoding='utf-8') == expected_content


def test_add_collection_raises_type_error(temp_dir):
    file_name = "test_set_file.txt"

    with SetFile(file_name, temp_dir) as set_file:
        # Attempt to add a collection that is neither a list nor a set
        with pytest.raises(TypeError):
            set_file.add_collection("not a list or set")  # Passing a string instead of list or set

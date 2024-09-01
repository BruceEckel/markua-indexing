from pathlib import Path
import pytest
from src.markua_indexing.markdown_doc import MarkdownDoc

TEST_DOC_CONTENT = 'This is a _test_ **Markdown** document.'
TEST_DOC_PATH = './test_doc.md'


# Set up test fixtures
@pytest.fixture
def mock_doc() -> MarkdownDoc:
    with open(TEST_DOC_PATH, 'w') as f:
        f.write(TEST_DOC_CONTENT)

    return MarkdownDoc(doc_path=Path(TEST_DOC_PATH))


# Tests start here
def test_markdown_doc_original(mock_doc: MarkdownDoc) -> None:
    assert mock_doc.original == TEST_DOC_CONTENT


def test_markdown_doc_codeless(mock_doc: MarkdownDoc) -> None:
    # Assuming strip_code function removes Markdown syntax
    assert mock_doc.codeless == 'This is a test Markdown document.'


def test_markdown_doc_italicized_phrases(mock_doc: MarkdownDoc) -> None:
    # Assuming italicized_phrases function extracts italicized phrases
    assert mock_doc.italicized_phrases == {'test'}


def test_markdown_doc_unique_words(mock_doc: MarkdownDoc) -> None:
    # Assuming unique_words function extracts unique words
    assert mock_doc.unique_words == {'this', 'is', 'a', 'test', 'markdown', 'document.'}


def test_markdown_doc_index_phrases(mock_doc: MarkdownDoc) -> None:
    # Assuming remove_stop_words function removes stop words ('is', 'a')
    assert mock_doc.index_phrases == {'test'}


def test_markdown_doc_index_words(mock_doc: MarkdownDoc) -> None:
    # Assuming remove_stop_words function removes stop words ('is', 'a')
    assert mock_doc.index_words == {'this', 'test', 'markdown', 'document.'}

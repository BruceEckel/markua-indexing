import pytest
from markua_indexing.generate_index_word_list import find_italicized_phrases


def test_single_asterisk():
    markdown = "This is *italic* text."
    expected = ["italic"]
    assert find_italicized_phrases(markdown) == expected


def test_single_underscore():
    markdown = "This is _italic_ text."
    expected = ["italic"]
    assert find_italicized_phrases(markdown) == expected


def test_mixed_italics():
    markdown = "This is *italic* and _also italic_ text."
    expected = ["italic", "also italic"]
    assert find_italicized_phrases(markdown) == expected


def test_no_italics():
    markdown = "This is plain text with no italics."
    expected = []
    assert find_italicized_phrases(markdown) == expected


def test_nested_italics():
    markdown = "This is *italic* and **bold** text with _italic_ as well."
    expected = ["italic", "italic"]
    assert find_italicized_phrases(markdown) == expected


def test_multiple_italic_phrases():
    markdown = "*First* phrase and _second_ phrase."
    expected = ["First", "second"]
    assert find_italicized_phrases(markdown) == expected


def test_escaped_italics():
    markdown = r"This is \*not italic\* and \_not italic\_."
    expected = []
    assert find_italicized_phrases(markdown) == expected


def test_italics_with_punctuation():
    markdown = "Here is *italic,* and _more italic!_"
    expected = ["italic,", "more italic!"]
    assert find_italicized_phrases(markdown) == expected


def test_incomplete_italics():
    markdown = "This is *incomplete and this is _also incomplete."
    expected = []
    assert find_italicized_phrases(markdown) == expected


def test_italicized_with_line_break():
    markdown = "This is *italic text\nwith a line break* and more text."
    expected = ["italic text\nwith a line break"]
    assert find_italicized_phrases(markdown) == expected


def test_italicized_with_line_break_underscores():
    markdown = "This is _italic text\nwith a line break_ and more text."
    expected = ["italic text\nwith a line break"]
    assert find_italicized_phrases(markdown) == expected

import pytest
from src.markua_indexing.generate_index_word_list import remove_fences

# List of test cases with markdown_text and expected_result pairs
test_cases = [

    ("""First line
```
This is a code block
```
Last line""", """First line

Last line"""),

    ("""First line
```
Code block 1
```
Middle line
```
Code block 2
```
Last line""", """First line

Middle line

Last line"""),

    ("""First line
Middle line
Last line""", """First line
Middle line
Last line"""),

    ("""First line
```python
Code block 1
```
Last line""",
     """First line

Last line""")
]


@pytest.mark.parametrize("markdown_text, expected_result", test_cases)
def test_remove_fences(markdown_text, expected_result):
    assert remove_fences(markdown_text) == expected_result

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MarkdownDoc:
    doc_path: Path
    original: str = field(init=False)
    codeless: str = field(init=False)
    italicized_phrases: list[str] = field(init=False)

    def __post_init__(self) -> None:
        self.original = self.doc_path.read_text(encoding='utf-8')
        self.codeless = strip_code(self.original)
        self.italicized_phrases = italicized_phrases(self.codeless)


def strip_code(source: str) -> str:
    """
    Returns the input string with all matching code blocks removed.
    - '\n```': Matches a newline followed by the opening triple backticks.
    - '.*?': Non-greedy match for any characters,
      including newlines (enabled by re.DOTALL).
    - '```': Matches the closing triple backticks.
    - '[^\n]*': Matches any non-newline characters after the closing backticks.
    """
    return re.sub(r'\n```.*?```[^\n]*', '', source, flags=re.DOTALL)


def italicized_phrases(source: str) -> list[str]:
    """
    source (str): The input string to search for italicized phrases.
    Returns:
    - list[str]: A list of all phrases found in the source string that
                 are italicized using either asterisks or underscores.
    """
    starred = r'\*.*?\*'
    underscored = r'_.*?_'
    starred_phrases = re.findall(starred, source, flags=re.DOTALL)
    underscored_phrases = re.findall(underscored, source, flags=re.DOTALL)
    return starred_phrases + underscored_phrases

def unique_words(source: str) -> list[str]:
    # Replace all non-word characters (punctuation, special characters)
    # with spaces, then break on spaces into words
    words = re.sub(r'\W+', ' ', source).split()
    # Filter out words that consist only of numbers
    non_numbers = [word for word in words if not word.isdigit()]
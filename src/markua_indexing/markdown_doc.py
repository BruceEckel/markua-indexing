import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Set

from markua_indexing.top_dir import TopDir

# Directory containing .txt files of words and phrases to exclude:
dictionaries = TopDir("dictionaries")
# Resulting words & phrases to index:
index_words_file = TopDir("index_words") / "index_words.txt"


@dataclass
class MarkdownDoc:
    doc_path: Path
    original: str = field(init=False)
    codeless: str = field(init=False)
    italicized_phrases: Set[str] = field(init=False)
    unique_words: Set[str] = field(init=False)
    index_phrases: Set[str] = field(init=False)
    index_words: Set[str] = field(init=False)

    def __post_init__(self) -> None:
        self.original = self.doc_path.read_text(encoding='utf-8')
        self.codeless = strip_code(self.original)
        self.italicized_phrases = italicized_phrases(self.codeless)
        self.unique_words = unique_words(self.codeless)
        self.index_phrases = remove_stop_words(self.italicized_phrases)
        self.index_words = remove_stop_words(self.unique_words)


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


def italicized_phrases(source: str) -> Set[str]:
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
    return set(starred_phrases) | set(underscored_phrases)


def unique_words(source: str) -> Set[str]:
    # Replace all non-word characters (punctuation, special characters)
    # with spaces, then break on spaces into words
    words = re.sub(r'\W+', ' ', source).split()
    # Filter out words that consist only of numbers
    non_numbers = [word for word in words if not word.isdigit()]
    # Produce a list of unique words sorted alphabetically
    return set(non_numbers)


def remove_stop_words(word_list: Set[str]) -> Set[str]:
    stop_words = set()

    # Dictionary lines starting with '#' are comments
    for dictionary in dictionaries.directory.glob("*.txt"):
        with dictionary.open(encoding='utf-8') as file:
            stop_words.update([line.strip().lower() for line in file
                               if not line.lstrip().startswith('#')])

    return {word for word in word_list if word.lower() not in stop_words}
    # return word_list - stop_words

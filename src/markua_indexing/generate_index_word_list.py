import argparse
import glob
import importlib.resources
import re
from pathlib import Path
from typing import List, Set

from markua_indexing.util import TopDir

stop_words_path = importlib.resources.files("markua_indexing.data").joinpath(
    "NLTKStopWords.txt"
)

index_words_file = TopDir("data") / "index_words.txt"


def remove_fences(markdown: str) -> str:
    pattern = r"(?s)```.*?\n.*?```"
    return re.sub(pattern, "", markdown)


def remove_fences_command_line():
    parser = argparse.ArgumentParser(description="Remove fenced code blocks from markdown files.")
    parser.add_argument("markdown_files", type=str, nargs='+', help="Paths to the markdown files (supports wildcards)")
    args = parser.parse_args()
    # Process each file matching the provided pattern(s)
    for pattern in args.markdown_files:
        for file_path in glob.glob(pattern):
            path = Path(file_path)
            if path.suffix == '.md':
                markdown_content = path.read_text(encoding='utf-8')
                de_fenced_content = remove_fences(markdown_content)
                # Create the new file name with '_de_fenced' appended before the file extension
                new_file_path = path.with_name(path.stem + '_de_fenced' + path.suffix)
                new_file_path.write_text(de_fenced_content, encoding='utf-8')
                print(f"Processed file saved as: {new_file_path}")


def find_italicized_phrases(markdown: str) -> List[str]:
    pattern = r"(?<!\*)\*(.*?)\*(?!\*)|(?<!_)_(.*?)_(?!_)"
    matches = re.findall(pattern, markdown)
    italic_phrases = [phrase for group in matches for phrase in group if phrase]
    return italic_phrases


def create_sorted_unique_word_list(text: str) -> List[str]:
    words = re.findall(r"\b\w+\b", text)
    unique_words: Set[str] = set(words)
    return sorted(unique_words, key=lambda word: (word.lower(), word))


def filter_stop_words(word_list: List[str]) -> List[str]:
    stop_words = set(stop_words_path.read_text(encoding="utf-8").splitlines())
    return [word for word in word_list if word.lower() not in stop_words]


import argparse
import glob
from pathlib import Path


def main():
    global index_words_file
    parser = argparse.ArgumentParser(
        description="""
    This script processes one or more markdown files, either individually named or via wildcard. 
    It reads each file, removes all fenced code blocks (delimited by ```), and extracts italicized phrases 
    (delimited by * or _). It accumulates all italicized phrases, generates a sorted list of unique words from 
    the remaining text, filters out stop words using a StopWords.txt file, and writes the result to index_words.txt.
    The italicized phrases are included at the top of index_words.txt.
    """
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="One or more markdown files or file patterns (wildcards supported).",
    )
    args = parser.parse_args()

    # Collect markdown files from the command line arguments (supporting wildcards)
    files = [file for arg in args.files for file in glob.glob(arg)]

    # To accumulate all italicized phrases as a set (unique phrases)
    all_italicized_phrases = set()

    # To accumulate all text after removing fences
    combined_text = ""

    for file in files:
        markdown_text = Path(file).read_text(encoding='utf-8')

        # Remove fenced code blocks
        de_fenced_text = remove_fences(markdown_text)

        # Find and accumulate italicized phrases
        all_italicized_phrases.update(find_italicized_phrases(de_fenced_text))

        # Accumulate the text for word processing
        combined_text += de_fenced_text + " "

    # Create a sorted unique word list from the combined de-fenced text
    sorted_unique_words = create_sorted_unique_word_list(combined_text)

    # Filter out stop words
    filtered_words = filter_stop_words(sorted_unique_words)

    with index_words_file.open("w", encoding='utf-8') as f:
        # Write italicized phrases at the top
        if all_italicized_phrases:
            f.write("Italicized Phrases:\n")
            f.write("\n".join(sorted(all_italicized_phrases)) + "\n\n")

        # Write the filtered words below the italicized phrases
        f.write("Index Words:\n")
        f.write("\n".join(filtered_words))

    # Optionally, you can print or log the italicized phrases if needed
    print(f"Collected italicized phrases: {all_italicized_phrases}")
    print(f"Filtered words have been written to {index_words_file}")


if __name__ == "__main__":
    main()

#: insert_codepath_tags.py
from pathlib import Path
from .markdown_file import MarkdownFile


def insert_codepath_tag(md: Path):
    markdown = MarkdownFile(md)
    for code_path in markdown.code_paths():
        print(code_path)

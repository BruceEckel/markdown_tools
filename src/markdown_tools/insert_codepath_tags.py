#: insert_codepath_tags.py
from pathlib import Path
from .markdown_file import MarkdownFile


def insert_codepath_tag(md: Path):
    md_file = MarkdownFile(md)
    for code_path in md_file.code_paths():
        md_file.display_name_once()
        print(code_path)

#: insert_codepath_tags.py
from pathlib import Path
from markdown_tools import MarkdownFile


def insert_codepath_tag(md: Path):
    md_file = MarkdownFile(md)
    for n, listing in enumerate(md_file.pathed_code_listings()):
        md_file.display_name_once()
        print(
            f"{n = } {listing.language}: {listing.source_file_name}"
        )
        if n == 0:
            idx = md_file.index_of(listing)
            print(f"{idx = }")

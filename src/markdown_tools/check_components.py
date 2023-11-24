# check_components.py
from pathlib import Path
from markdown_tools import MarkdownFile, SourceCode, Comment, CodePath


def check_code_block(scl: SourceCode) -> str | None:
    if scl.language == "text" or scl.ignore:
        return None
    return f"{scl.language}: {scl.source_file_name}"


def check_code_listings(md: Path):
    for listing in MarkdownFile(md).code_listings():
        assert isinstance(listing, SourceCode)
        r = check_code_block(listing)
        if r:
            print(r)


def check_markdown_comments(md: Path):
    print(f"{md}:")
    for comment in MarkdownFile(md).comments():
        assert isinstance(comment, Comment) or isinstance(
            comment, CodePath
        )
        print(comment)

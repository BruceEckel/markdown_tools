# update_listings.py
from pathlib import Path
from markdown_tools import (
    MarkdownFile,
    SourceCode,
    Comment,
    CodePath,
    console,
)


def compare_listings_to_source_files(md: Path):
    md_file = MarkdownFile(md)
    md_file.display_name_once()
    for code_path, source_code in md_file.code_path_and_source_code():
        full_path = Path(code_path.path) / Path(  # type: ignore
            source_code.source_file_name
        )
        assert (
            full_path.exists()
        ), f"ERROR: {full_path.as_posix()} does not exist"
        console.print(f"{full_path.as_posix()} ", end="")
        source_file = SourceCode.from_source_file(full_path)
        if source_file == source_code:
            console.print("\n[MATCH]")
        else:
            console.print("\n[NO MATCH]")
            console.print("Listing:\n", source_code)
            console.print("*" * 50)
            console.print("Source file:\n", source_file)
            console.print("^" * 50)


def update_listings(md: Path):
    md_file = MarkdownFile(md)
    md_file.display_name_once()
    for code_path, source_code in md_file.code_path_and_source_code():
        full_path = Path(code_path.path) / Path(  # type: ignore
            source_code.source_file_name
        )
        assert (
            full_path.exists()
        ), f"ERROR: {full_path.as_posix()} does not exist"
        source_file = full_path.read_text(encoding="utf-8")
        if source_file != source_code.code:
            console.print(f"Updating from {full_path.as_posix()}")
            # 1. Create a new SourceCode object from source_file
            # 2. md_file[md_file.index_of(source_code)] = new_source_code


def check_code_block(scl: SourceCode) -> str | None:
    if scl.language_name == "text" or scl.ignore:
        return None
    return f"{scl.language_name}: {scl.source_file_name}"


def check_code_listings(md: Path):
    md_file = MarkdownFile(md)
    for listing in md_file.code_listings():
        assert isinstance(listing, SourceCode)
        if r := check_code_block(listing):
            md_file.display_name_once()
            console.print(r)


def display_markdown_comments(md: Path):
    console.print(f"{md}:")
    for comment in MarkdownFile(md).comments():
        assert isinstance(comment, Comment) or isinstance(
            comment, CodePath
        )
        console.print(comment)

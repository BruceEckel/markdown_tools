# check_components.py
from pathlib import Path
from markdown_tools import MarkdownFile, SourceCode, Comment, CodePath


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
        print(f"{full_path.as_posix()} ", end="")
        source_file = full_path.read_text(encoding="utf-8")
        if source_file == source_code.code:
            print("[MATCH]")
        else:
            print("[NO]")
            print("Listing:\n", source_code.code)
            print("*" * 50)
            print("Original file:\n", source_file)
            print("^" * 50)


def check_code_block(scl: SourceCode) -> str | None:
    if scl.language == "text" or scl.ignore:
        return None
    return f"{scl.language}: {scl.source_file_name}"


def check_code_listings(md: Path):
    md_file = MarkdownFile(md)
    for listing in md_file.code_listings():
        assert isinstance(listing, SourceCode)
        if r := check_code_block(listing):
            md_file.display_name_once()
            print(r)


def check_markdown_comments(md: Path):
    print(f"{md}:")
    for comment in MarkdownFile(md).comments():
        assert isinstance(comment, Comment) or isinstance(
            comment, CodePath
        )
        print(comment)

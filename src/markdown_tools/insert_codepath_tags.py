#: insert_codepath_tags.py
from pathlib import Path
from markdown_tools import MarkdownFile, CodePath, SourceCode
import typer

code_paths = {
    "python": "C:/git/python-experiments",
    "rust": "C:/git/rust-experiments",
    "go": "C:/git/go-experiments",
}


def find_file(start_path: Path, file_name: str) -> Path | None:
    # Search recursively for the file:
    for path in start_path.rglob(file_name):
        return path  # First match
    return None  # No file found


def validated_codepath(
    guess: str | CodePath, file_name: str
) -> Path | None:
    assert isinstance(guess, str) or isinstance(guess, CodePath)
    if isinstance(guess, str):
        guess_path = Path(guess)
    elif isinstance(guess, CodePath):
        guess_path = Path(guess.path)

    for path in Path(guess_path).rglob(file_name):
        return path.parent  # First match
    return None  # No file found


def insert_codepath_tags(md: Path):
    md_file = MarkdownFile(md)
    tmp_file = md_file.file_path.with_suffix(".tmp.md")
    if tmp_file.exists():
        print(f"Deleting: {tmp_file}")
        tmp_file.unlink()
    code_path: CodePath | None = None
    for part in md_file:
        if isinstance(part, CodePath):
            code_path = part  # Most recent CodePath
        if (
            isinstance(part, SourceCode)
            and not part.language == "text"
            and not part.ignore
        ):
            if code_path:
                if validated_codepath(
                    code_path, part.source_file_name
                ):
                    print(
                        f"Validated {code_path} for {part.source_file_name}"
                    )
                else:
                    typer.Exit(
                        f"Failed: {code_path} for {part.source_file_name}"
                    )
            else:  # No prior code_path, make one
                if validated := validated_codepath(
                    code_paths[part.language], part.source_file_name
                ):
                    idx = md_file.index_of(part)
                    code_path = CodePath.new(md_file, validated)
                    md_file.insert(idx, code_path)
                    md_file.write_new_file(tmp_file)
                else:
                    typer.Exit(
                        f"Failed: {code_paths[part.language]} for {part.source_file_name}"
                    )


def insert_codepath_tag(md: Path):
    md_file = MarkdownFile(md)
    tmp_file = md_file.file_path.with_suffix(".tmp.md")
    if tmp_file.exists():
        print(f"Deleting: {tmp_file}")
        tmp_file.unlink()
    if CodePath in md_file:
        return  # Contains a CodePath, no need to add one
    for n, listing in enumerate(md_file.pathed_code_listings()):
        md_file.display_name_once()
        print(
            f"{n = } {listing.language}: {listing.source_file_name}"
        )
        if n == 0:  # Only do it for the first listing
            start_path = Path(code_paths[listing.language])
            if found_path := find_file(
                start_path, listing.source_file_name
            ):
                idx = md_file.index_of(listing)
                code_path = CodePath.new(
                    md_file, Path(found_path.parent)
                )
                md_file.insert(idx, code_path)
                md_file.write_new_file(tmp_file)
            else:
                md_file.md_source.assert_true(
                    False,
                    f"Couldn't locate file beneath {start_path}",
                )

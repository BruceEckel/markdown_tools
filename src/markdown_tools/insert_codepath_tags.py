#: insert_codepath_tags.py
from pathlib import Path
from markdown_tools import MarkdownFile, CodePath

code_paths = {
    "python": "C:/git/python-experiments",
    "rust": "C:/git/rust-experiments",
    "go": "C:/git/go-experiments",
}


def find_file(start_path: Path, file_name: str) -> Path | None:
    # Use rglob to search recursively for the file
    for path in start_path.rglob(file_name):
        return path  # Return the first match
    return None  # If no file is found


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

#: insert_codepath_tags.py
from pathlib import Path
from markdown_tools import MarkdownFile, CodePath, SourceCode
import typer
from .markdown_file import starting_code_path


# def find_file(start_path: Path, file_name: str) -> Path | None:
#     # Search recursively for the file:
#     for path in start_path.rglob(file_name):
#         return path.parent  # First match
#     return None  # No file found


# def validated_codepath(
#     start: str | CodePath, file_name: str
# ) -> Path | None:
#     assert isinstance(start, str) or isinstance(start, CodePath)
#     if isinstance(start, str):
#         start_path = Path(start)
#     elif isinstance(start, CodePath):
#         start_path = Path(str(start.path))

#     for path in start_path.rglob(file_name):
#         return path.parent  # First match
#     return None  # No file found


def validate_codepath_tags(md: Path):
    md_file = MarkdownFile(md)
    code_path: CodePath | None = None
    for part in md_file:
        if isinstance(part, CodePath):
            code_path = part  # Most recent CodePath
        if (
            isinstance(part, SourceCode)
            and not part.language == "text"
            and not part.ignore
        ):
            md_file.display_name_once()
            if code_path is None:
                print(
                    "[FAILED] validate_codepath_tags(): "
                    f"{part.source_file_name} appeared before CodePath"
                )
                continue
            if full_path := code_path.validate(part):
                print(
                    f"Validated {code_path.path} -> {part.source_file_name}\n"
                    f"full_path: {full_path.as_posix()}"
                )
            else:
                print(
                    f"Invalid: {part.source_file_name} under {code_path.path}"
                )


def insert_codepath_tags(md: Path):
    md_file = MarkdownFile(md)
    md_file.display_name_once()
    tmp_file = md_file.file_path.with_suffix(".tmp.md")
    if tmp_file.exists():
        print(f"Deleting: {tmp_file}")
        tmp_file.unlink()
    code_path: CodePath | None = None
    for part in md_file:
        if isinstance(part, CodePath):
            code_path = part  # Most recent CodePath
            continue
        if (
            isinstance(part, SourceCode)
            and part.language != "text"
            and not part.ignore
        ):
            source_code: SourceCode = part
            if code_path and code_path.validate(source_code):
                print(
                    f"Validated {code_path.path} -> {source_code.source_file_name}"
                )
            else:  # code_path None or didn't validate.
                # Insert a new one before source_code
                code_path = CodePath.new_based_on(source_code)
                idx = md_file.index_of(source_code)
                md_file.insert(idx, code_path)
                md_file.write_new_file(tmp_file)


# def insert_codepath_tag(md: Path):
#     md_file = MarkdownFile(md)
#     tmp_file = md_file.file_path.with_suffix(".tmp.md")
#     if tmp_file.exists():
#         print(f"Deleting: {tmp_file}")
#         tmp_file.unlink()
#     if md_file.contains(CodePath):  # type: ignore
#         return  # Contains a CodePath, no need to add one
#     for n, listing in enumerate(md_file.pathed_code_listings()):
#         md_file.display_name_once()
#         print(
#             f"{n = } {listing.language}: {listing.source_file_name}"
#         )
#         if n == 0:  # Only do it for the first listing
#             start_path = Path(starting_code_path[listing.language])
#             if found_path := find_file(
#                 start_path, listing.source_file_name
#             ):
#                 idx = md_file.index_of(listing)
#                 code_path = CodePath.new(
#                     md_file, found_path.parent.as_posix()
#                 )
#                 md_file.insert(idx, code_path)
#                 md_file.write_new_file(tmp_file)
#             else:
#                 md_file.md_source.assert_true(
#                     False,
#                     f"Couldn't locate file beneath {start_path}",
#                 )

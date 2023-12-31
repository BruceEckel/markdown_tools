#: insert_codepath_tags.py
from pathlib import Path
from .markdown_file import MarkdownFile, CodePath, SourceCode
from .console import console


def validate_codepath_tags(md: Path):
    md_file = MarkdownFile(md)
    code_path: CodePath | None = None
    for part in md_file:
        if isinstance(part, CodePath):
            code_path = part  # Most recent CodePath
        if (
            isinstance(part, SourceCode)
            and not part.language_name == "text"
            and not part.ignore
        ):
            md_file.display_name_once()
            if code_path is None:
                console.print(
                    "[FAILED] validate_codepath_tags(): "
                    f"{part.source_file_name} appeared before CodePath"
                )
                continue
            if code_path.validate(part):
                console.print(
                    f"Validated {code_path.path} -> {part.source_file_name}"
                )
            else:
                console.print(
                    f"Invalid: {part.source_file_name} under {code_path.path}"
                )


def insert_codepath_tags(md: Path):
    md_file = MarkdownFile(md)
    code_path: CodePath | None = None
    md_file.display_name_once()
    tmp_file = md_file.file_path.with_suffix(".tmp.md")
    if tmp_file.exists():
        console.print(f"Deleting: {tmp_file}")
        tmp_file.unlink()
    for part in md_file:
        if isinstance(part, CodePath):
            code_path = part  # Most recent CodePath
            continue
        if (
            isinstance(part, SourceCode)
            and part.language_name != "text"
            and not part.ignore
        ):
            source_code: SourceCode = part
            if code_path and code_path.validate(source_code):
                console.print(
                    f"Validated {code_path.path} -> {source_code.source_file_name}"
                )
            else:  # code_path is None or didn't validate.
                # Insert a new one before source_code
                code_path = CodePath.new_based_on(source_code)
                idx = md_file.index_of(source_code)
                md_file.insert(idx, code_path)
                md_file.write_new_file(md_file.file_path)

# update_listings.py
from difflib import context_diff
from pathlib import Path
from markdown_tools import (
    MarkdownFile,
    SourceCode,
    Comment,
    CodePath,
    console,
)
from rich.panel import Panel
import difflib


def compare_strings(str1: str, str2: str):
    n1, n2 = 1, 1
    result = []

    for line in list(
        difflib.Differ().compare(str1.splitlines(), str2.splitlines())
    ):
        if line.startswith("  "):
            # Line present in both strings
            result.append(f"  {n1:4} {n2:4} {line}")
            n1 += 1
            n2 += 1
        elif line.startswith("- "):
            # Line present in str1 but not in str2
            result.append(f"- {n1:4}      {line}")
            n1 += 1
        elif line.startswith("+ "):
            # Line present in str2 but not in str1
            result.append(f"+      {n2:4} {line}")
            n2 += 1

    return result


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
        console.rule(f"{full_path.as_posix()}", align="left")
        source_file = SourceCode.from_source_file(full_path)
        if source_file == source_code:
            console.print("[green bold][MATCH]")
        else:
            console.print("[red bold][DOES NOT MATCH]")
            console.print("In Markdown:", source_code)
            console.print("Source code file:", source_file)
            diff = compare_strings(
                source_code.code,
                source_file.code,
            )
            console.print(
                Panel(
                    "\n".join(diff), title="Diff: Markdown <-> Source"
                )
            )


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

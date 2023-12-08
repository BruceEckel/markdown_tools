# update_listings.py
from pathlib import Path
from .markdown_file import (
    MarkdownFile,
    SourceCode,
    Comment,
    CodePath,
    check,
)
from rich.panel import Panel, Text
from rich.console import group
from rich.prompt import Prompt, Confirm
from .console import console
from .compare_strings import compare_strings, DiffResult
from .vscode_open import vscode_open


def compare_listings_to_source_files(
    md: Path, file_edit_script: Path
) -> None:
    md_file = MarkdownFile(md)
    md_file.display_name_once()
    for code_path, source_code in md_file.code_path_and_source_code():
        full_path = Path(code_path.path) / Path(  # type: ignore
            source_code.source_file_name
        )
        check.is_true(
            full_path.exists(),
            f"{full_path.as_posix()} does not exist",
        )

        def show_result(title: str, border_color: str = "cadet_blue"):
            console.print(
                Panel(
                    Text(full_path.as_posix(), style="green"),
                    title=title,
                    title_align="left",
                    border_style=border_color,
                )
            )

        source_file = SourceCode.from_source_file(full_path)
        diff = compare_strings(source_code.code, source_file.code)

        match diff.result:
            case DiffResult.NONE:
                assert source_file == source_code
                show_result("[turquoise2 bold][MATCH]")
            case DiffResult.BLANK_LINES:
                show_result("[green3][BLANK LINES ONLY CHANGED]")
                diff.show()
                Prompt.ask("CR to continue")
            case DiffResult.CONTENT:
                vscode_open(file_edit_script, full_path)
                show_result("[bright_red][CONTENT DIFFERENCE]")
                diff.show()
                Confirm.ask("Continue")


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


def display_markdown_comments(md: Path):
    @group()
    def parts():
        for comment in MarkdownFile(md).comments():
            assert isinstance(comment, Comment) or isinstance(
                comment, CodePath
            )
            yield comment

    console.print(
        Panel(
            parts(),
            title=f"{md}",
            border_style="yellow",
            title_align="left",
        )
    )
    console.print()

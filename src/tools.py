#: tools.py
"""
Tests and maintains Markdown files containing embedded code listings.
"""
import os
import platform
import subprocess
from pathlib import Path
from typing import Callable, List, Optional

import typer
from markdown_tools.check_markdown import check_markdown
from markdown_tools.console import console
from markdown_tools.display_comments import display_markdown_comments
from markdown_tools.edit_changed_examples import edit_example_changes
from markdown_tools.insert_codepath_tags import (
    insert_codepath_tags,
    validate_codepath_tags,
)
from markdown_tools.numbered_file import NumberedFile
from markdown_tools.update_examples import (
    update_examples_from_source_code,
)
from rich.panel import Panel, Text
from typing_extensions import Annotated

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h"]},
    rich_markup_mode="rich",
)


def process_files(
    filename: Optional[str],
    processor: Callable[..., None],
    *args,
    **kwargs,
) -> None:
    """
    Process a single file or all Markdown files in the current directory
    using the provided processor function.
    """
    if filename:
        processor(Path(filename), *args, **kwargs)
    else:
        for md in Path(".").glob("*.md"):
            processor(md, *args, **kwargs)


def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")


def display(msg: str, style: str = "green") -> None:
    console.print(Panel(Text(msg, style=style)))


def run_powershell(script_path: Path):
    command = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
    ]
    try:
        subprocess.run(
            command, check=True, text=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)


@app.command("1", rich_help_panel="Validation")
def basic(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Basic validation of Markdown files
    """
    for tmp_file in Path(".").glob("*.tmp.md"):
        console.print(f"Removing {tmp_file.name}")
        tmp_file.unlink()

    def _check(md: Path):
        console.print(f"{md.name} ", end="")
        assert md.exists(), f"{md} does not exist"
        console.print(check_markdown(md))

    process_files(filename, _check)


@app.command("2", rich_help_panel="Validation")
def show_special_comments(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    "Display Markdown Comments that follow special format"
    process_files(filename, display_markdown_comments)


@app.command("3", rich_help_panel="Validation")
def verify_code_paths(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Verify code path comment tags are correct
    """
    process_files(filename, validate_codepath_tags)


@app.command("4", rich_help_panel="Validation")
def vscode_on_changes(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Opens VSCode on changed examples in source code files
    """
    file_edit_script = Path("edit_changed_files.ps1")
    if file_edit_script.exists():
        file_edit_script.unlink()

    process_files(filename, edit_example_changes, file_edit_script)

    if file_edit_script.exists():
        display(f"Executing {file_edit_script}")
        run_powershell(file_edit_script)
    else:
        display("No content differences found.")


@app.command("5", rich_help_panel="Modification")
def update_examples(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Updates examples in markdown from source code files
    """
    process_files(filename, update_examples_from_source_code)


@app.command("6", rich_help_panel="Modification")
def insert_codepaths(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None,
):
    """
    Insert code path comment tag in a file that doesn't have one
    """
    process_files(filename, insert_codepath_tags)


@app.command("7", rich_help_panel="Modification")
def renumber_chapters(
    go: Annotated[
        Optional[str],
        typer.Argument(help="'go': perform the changes"),
    ] = None
):
    """
    Reorders numbered Markdown files. To insert a file numbered 'n',
    name it 'n.! Chapter Title'. The '!' gives that chapter
    priority over another chapter with the same number.
    No flag: show what will be done. 'go' flag: do it.
    """
    go_flag = False
    if go:
        if go == "go":
            go_flag = True
        else:
            console.print("use 'go' argument to execute changes")
            raise typer.Exit()
    chapter_changes: List[
        NumberedFile
    ] = NumberedFile.chapters().changes
    appendix_changes: List[
        NumberedFile
    ] = NumberedFile.appendices().changes
    if not chapter_changes and not appendix_changes:
        console.print("No Changes")

    def make_changes(changes: List[NumberedFile]):
        for change in changes:
            console.print(
                f"'{change.original_name}'  -->  '{change.new_name}'"
            )
            if go_flag:
                os.rename(change.original_name, change.new_name)

    make_changes(chapter_changes)
    make_changes(appendix_changes)


# @callback used here only to produce the __doc__ string
@app.callback()
def doc():
    """
    Utilities for managing computer programming books written in Markdown
    """


# @app.command("m", rich_help_panel="Menu")
# def menu_callback(value: bool):
#     if value:
#         print("Menu Callback")
#         raise typer.Exit()


def main(
    # menu: Annotated[
    #     Optional[bool],
    #     typer.Option("--menu", callback=menu_callback),
    # ] = None,
):
    clear_screen()
    app()


if __name__ == "__main__":
    main()

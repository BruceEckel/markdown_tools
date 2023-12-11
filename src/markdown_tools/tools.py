#: tools.py
"""
Tests and maintains Markdown files containing embedded code listings.
"""
import os
from typing import List, Optional
from typing_extensions import Annotated
from pathlib import Path
import platform
import typer
from markdown_tools.console import console
from markdown_tools.check_markdown import check_markdown
from markdown_tools.insert_codepath_tags import (
    insert_codepath_tags,
    validate_codepath_tags,
)
from markdown_tools.numbered_file import NumberedFile
from markdown_tools.edit_changed_examples import edit_example_changes
from markdown_tools.update_examples import (
    update_examples_with_source_code,
)
from markdown_tools.display_comments import display_markdown_comments

# import readchar

clear_screen = "cls" if platform.system() == "Windows" else "clear"

cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h"]},
)


@cli.command()
def a(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Basic validation of Markdown files.
    """
    for tmp_file in Path(".").glob("*.tmp.md"):
        console.print(f"Removing {tmp_file.name}")
        tmp_file.unlink()

    def _check(md: Path):
        console.print(f"{md.name} ", end="")
        assert md.exists(), f"{md} does not exist"
        console.print(check_markdown(md))

    if filename:
        _check(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            _check(md)


@cli.command()
def b(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    List parsed comments
    """
    if filename:
        display_markdown_comments(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            display_markdown_comments(md)


@cli.command()
def c(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Edits changed examples in source code files.
    """
    file_edit_script = Path("edit_changed_files.ps1")
    if file_edit_script.exists():
        file_edit_script.unlink()
    if filename:
        edit_example_changes(Path(filename), file_edit_script)
    else:
        for md in Path(".").glob("*.md"):
            edit_example_changes(md, file_edit_script)


@cli.command()
def d(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Updates examples in markdown from source code files.
    """
    file_edit_script = Path("edit_changed_files.ps1")
    if file_edit_script.exists():
        file_edit_script.unlink()
    if filename:
        update_examples_with_source_code(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            update_examples_with_source_code(md)


@cli.command()
def e(
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


@cli.command()
def f(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Verify code path comment tags are correct.
    """
    if filename:
        validate_codepath_tags(Path(filename))
    else:
        for md in [
            p for p in Path(".").glob("*.md") if ".tmp" not in p.name
        ]:
            validate_codepath_tags(md)


@cli.command()
def g(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Insert code path comment tag in a file that doesn't have one.
    """
    if filename:
        insert_codepath_tags(Path(filename))
    else:
        for md in [
            p for p in Path(".").glob("*.md") if ".tmp" not in p.name
        ]:
            insert_codepath_tags(md)


def main():
    """Called in pyproject.toml:
    [project.scripts]
    mt = "markdown_tools.tools:main"
    """
    os.system(clear_screen)
    cli()


if __name__ == "__main__":
    main()

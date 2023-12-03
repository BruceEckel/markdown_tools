#: tools.py
"""
Tests and maintains Markdown files containing embedded code listings.
"""
import os
import typer
from typing import List, Optional
from typing_extensions import Annotated
from markdown_tools import (
    display_markdown_comments,
    check_markdown,
    insert_codepath_tags,
    validate_codepath_tags,
    NumberedFile,
)
from pathlib import Path
import platform
from .console import console

from markdown_tools.update_listings import (
    compare_listings_to_source_files,
    update_listings,
)

clear_screen = "cls" if platform.system() == "Windows" else "clear"

cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h"]},
)


@cli.command()
def a_check(
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
def b_check_comments(
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
def c_listings(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Validates code listings within Markdown files.
    """
    if filename:
        compare_listings_to_source_files(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            compare_listings_to_source_files(md)


@cli.command()
def d_update_listings(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Updates code listings from source code files.
    """
    if filename:
        update_listings(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            update_listings(md)


@cli.command()
def e_renumber(
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
def f_validate_code_paths(
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
def g_insert_code_paths(
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
    os.system(clear_screen)
    cli()


if __name__ == "__main__":
    main()

#: tools.py
"""
Tests and maintains Markdown files containing embedded code listings.
"""
import os
import typer
from typing import List, Optional
from typing_extensions import Annotated
from markdown_tools import (
    check_code_listings,
    check_markdown_comments,
    check_markdown,
    insert_codepath_tag,
    NumberedFile,
)
from pathlib import Path
import platform


clear_screen = "cls" if platform.system() == "Windows" else "clear"


cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h"]},
)


@cli.command()
def check(
    filename: Annotated[
        Optional[str],
        typer.Argument(
            help="Markdown file to check (None: all files)"
        ),
    ] = None
):
    """
    Validates Markdown files.
    """

    for tmp_file in Path(".").glob("*.mtmp"):
        print(f"Removing {tmp_file.name}")
        tmp_file.unlink()

    def _check(md: Path):
        print(f"{md.name} ", end="")
        assert md.exists(), f"{md} does not exist"
        print(f"[{check_markdown(md)}]")

    if filename:
        _check(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            _check(md)


@cli.command()
def check_comments(
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

    def _check(md: Path):
        print(f"{md.name} ", end="")
        assert md.exists(), f"{md} does not exist"
        print(f"[{check_markdown(md)}]")

    if filename:
        check_markdown_comments(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            check_markdown_comments(md)


@cli.command()
def listings(
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
        check_code_listings(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            check_code_listings(md)


@cli.command()
def insert_code_paths(
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
        insert_codepath_tag(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            insert_codepath_tag(md)


@cli.command()
def renumber(
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
            print("use 'go' argument to execute changes")
            raise typer.Exit()
    chapter_changes: List[
        NumberedFile
    ] = NumberedFile.chapters().changes
    appendix_changes: List[
        NumberedFile
    ] = NumberedFile.appendices().changes
    if not chapter_changes and not appendix_changes:
        print("No Changes")

    def make_changes(changes: List[NumberedFile]):
        for change in changes:
            print(
                f"'{change.original_name}'  -->  '{change.new_name}'"
            )
            if go_flag:
                os.rename(change.original_name, change.new_name)

    make_changes(chapter_changes)
    make_changes(appendix_changes)


def main():
    os.system(clear_screen)
    cli()


if __name__ == "__main__":
    main()

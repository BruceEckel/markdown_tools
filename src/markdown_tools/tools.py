"""
Tests and maintains Markdown files containing embedded code listings.
"""
import os
import typer
from typing import List, Optional
from typing_extensions import Annotated
from markdown_tools import (
    separator,
    check_code_listings,
    check_markdown,
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
        assert md.exists(), f"{md} does not exist"
        print(f"{md.name}: [{check_markdown(md)}]")

    if filename:
        _check(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            _check(md)


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

    def _check(md: Path):
        assert md.exists(), f"{md} does not exist"
        print(separator(md.name, "-"), end="")
        check_code_listings(md)

    if filename:
        _check(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            _check(md)


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

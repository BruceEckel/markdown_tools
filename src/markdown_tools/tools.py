"""
Tests and maintains Markdown files containing embedded code listings.
"""
import sys
import typer
from typing import Optional
from typing_extensions import Annotated
from markdown_tools import (
    separator,
    check_code_listings,
    check_markdown,
    NumberedFile,
)
from pathlib import Path

app = typer.Typer(
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h"]},
)


@app.command()
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

    def _check(md: Path):
        assert md.exists(), f"{md} does not exist"
        print(f"{md.name}: [{check_markdown(md)}]")

    if filename:
        _check(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            _check(md)


@app.command()
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
        print(separator(md, "+"), end="")
        check_code_listings(md)

    if filename:
        _check(Path(filename))
    else:
        for md in Path(".").glob("*.md"):
            _check(md)


@app.command()
def renumber(
    go: Annotated[
        Optional[str],
        typer.Argument(help="'go': perform the changes"),
    ] = None
):
    """
    Reorders numbered Markdown files. To insert a file 'n',
    name it 'n.! Chapter Title'. The '!' gives that chapter
    priority over another chapter with the same number.
    TODO: No flag: show what will be done. Flag: do it.
    """
    chapter_changes = NumberedFile.chapters().changes
    appendix_changes = NumberedFile.appendices().changes
    if not chapter_changes and not appendix_changes:
        print("No Changes")
    for chapter in NumberedFile.chapters().changes:
        # print(chapter)
        print(f"'{chapter.original_name}'  -->  '{chapter.new_name}'")
        # os.rename(chapter.original_name, chapter.new_name)
    for appendix in NumberedFile.appendices().changes:
        # print(appendix)
        print(
            f"'{appendix.original_name}'  -->  '{appendix.new_name}'"
        )
        # os.rename(appendix.original_name, appendix.new_name)


def main():
    app()


if __name__ == "__main__":
    main()

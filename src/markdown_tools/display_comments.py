# display_comments.py
from pathlib import Path
from markdown_tools.markdown_file import (
    MarkdownFile,
    Comment,
    CodePath,
)
from rich.panel import Panel
from rich.console import group
from markdown_tools.console import console


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

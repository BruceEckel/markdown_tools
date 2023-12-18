# compare_strings.py
import difflib
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from markdown_tools.markdown_file import MarkdownFile
from .console import console
from rich.panel import Panel, Text


class DiffResult(Enum):
    NONE = "[turquoise2 bold][MATCH]"
    BLANK_LINES = "[green3][BLANK LINES ONLY CHANGED]"
    CONTENT = "[bright_red][CONTENT DIFFERENCE]"


@dataclass
class CompareResult:
    result: DiffResult
    diffs: list[str]

    def show_diffs(self, md_file: MarkdownFile) -> None:
        md_file.display_name_once()
        console.print(
            Panel(
                "\n".join(self.diffs),
                title="[gold3]Diff: [dark_red]Markdown[/dark_red] <-> [dark_magenta]Source",
                title_align="left",
                border_style="steel_blue3",
            )
        )

    def show_result(self, path: Path) -> None:
        console.print(
            Panel(
                Text(path.as_posix(), style="green"),
                title=self.result.value,
                title_align="left",
                border_style="cadet_blue",
            )
        )


def only_differs_by_blank_lines(str1: str, str2: str) -> bool:
    def no_blank_lines(with_blanks: str) -> list[str]:
        return [
            line
            for line in with_blanks.splitlines(True)
            if line.strip()
        ]

    return no_blank_lines(str1) == no_blank_lines(str2)


def create_diffs(str1: str, str2: str) -> list[str]:
    differences: list[str] = []
    n1, n2 = 1, 1
    diffs = list(
        difflib.Differ().compare(str1.splitlines(), str2.splitlines())
    )
    for line in diffs:
        if line.startswith("  "):
            # Line present in both strings
            differences.append(f"  {n1:4} {n2:4} {line}")
            n1 += 1
            n2 += 1
        elif line.startswith("- "):
            # Line present in str1 but not in str2
            differences.append(
                f"[dark_red]- {n1:4}      {line}[/dark_red]"
            )
            n1 += 1
        elif line.startswith("+ "):
            # Line present in str2 but not in str1
            differences.append(
                f"[dark_magenta]+      {n2:4} {line}[/dark_magenta]"
            )
            n2 += 1
    return differences


def compare_strings(str1: str, str2: str) -> CompareResult:
    diffs = create_diffs(str1, str2)

    if str1 == str2:
        return CompareResult(DiffResult.NONE, diffs)

    if only_differs_by_blank_lines(str1, str2):
        return CompareResult(DiffResult.BLANK_LINES, diffs)

    return CompareResult(DiffResult.CONTENT, diffs)

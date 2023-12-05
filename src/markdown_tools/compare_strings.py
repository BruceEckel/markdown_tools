# compare_strings.py
import difflib
from enum import Enum
from dataclasses import dataclass


class DiffResult(Enum):
    NONE = "No difference"
    BLANK_LINES = "Only blank lines added/subtracted"
    CONTENT = "Content difference"


@dataclass
class CompareResult:
    result: DiffResult
    diffs: list[str]


def only_differs_by_blank_lines(str1: str, str2: str) -> bool:
    def no_blank_lines(with_blanks: str) -> list[str]:
        return [
            line
            for line in with_blanks.splitlines(True)
            if line.strip()
        ]

    return no_blank_lines(str1) == no_blank_lines(str2)


def create_diffs(str1: str, str2: str) -> list[str]:
    differences = []
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

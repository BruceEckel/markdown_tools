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


def compare_strings(str1: str, str2: str) -> CompareResult:
    n1, n2 = 1, 1
    differences = []
    result = DiffResult.NONE

    for line in list(
        difflib.Differ().compare(str1.splitlines(), str2.splitlines())
    ):
        if line.startswith("  "):
            # Line present in both strings
            differences.append(f"  {n1:4} {n2:4} {line}")
            n1 += 1
            n2 += 1
        elif line.startswith("- "):
            # Line present in str1 but not in str2
            differences.append(f"- {n1:4}      {line}")
            n1 += 1
            if result == DiffResult.NONE:
                result = DiffResult.BLANK_LINES
            if not line.isspace():
                result = DiffResult.CONTENT
        elif line.startswith("+ "):
            # Line present in str2 but not in str1
            differences.append(f"+      {n2:4} {line}")
            n2 += 1
            if result == DiffResult.NONE:
                result = DiffResult.BLANK_LINES
            if not line.isspace():
                result = DiffResult.CONTENT

    return CompareResult(result=result, diffs=differences)

# error_reporter.py
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import typer


@dataclass
class ErrorReporter:
    """
    Only if information is available is it displayed
    """

    source_file: Path | None = None
    # Line number starting current analysis block:
    context_start: int | None = None
    markdown_part: Any = None  # (Circular import problem)

    def assert_true(self, condition: bool, msg: str) -> None:
        if not condition:
            raise typer.Exit(self.format_error(msg))  # type: ignore

    def format_error(self, msg: str) -> str:
        _msg = "[ERROR]"
        if sf := self.source_file:
            _msg += f" in {sf}"
        if cs := self.context_start:
            _msg += f" starting at line {cs}"
        if mp := self.markdown_part:
            _msg += f"\n{mp}"
        return _msg + ":\n" + msg

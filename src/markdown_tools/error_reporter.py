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

    # Markdown file currently being parsed:
    md_source_file: Path | None = None
    # Class we are currently inside:
    klass: str | None = None
    # function or method we are currently inside:
    function: str | None = None
    # Line number in md_source_file starting current analysis block:
    context_start: int | None = None
    markdown_part: Any = None

    def assert_true(self, condition: bool, msg: str) -> None:
        if not condition:
            raise typer.Exit(self.format_error(msg))  # type: ignore

    def format_error(self, msg: str) -> str:
        _msg = "[ERROR]"
        if sf := self.md_source_file:
            _msg += f" in {sf}"
        if cls := self.klass:
            _msg += f" in {cls}"
        if fn := self.function:
            _msg += f" in {fn}"
        if cs := self.context_start:
            _msg += f" starting at line {cs}"
        if mp := self.markdown_part:
            _msg += f"\n{mp}"
        return _msg + ":\n" + msg

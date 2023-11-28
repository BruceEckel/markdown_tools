#: util.py
from dataclasses import dataclass
from pathlib import Path
import typer


def separator(id: str, sep_char: str = "-") -> str:
    BEGIN = 5
    WIDTH = 50
    start = f"{sep_char * BEGIN} {id} "
    return start + f"{(WIDTH - len(start)) * sep_char}" + "\n"


@dataclass
class ErrorReporter:
    """
    Only if information is available is it displayed
    """

    source_file: Path | None = None
    # Line number starting current analysis block:
    context_start: int | None = None
    klass: str | None = None
    function: str | None = None

    def assert_true(self, condition: bool, msg: str) -> None:
        if not condition:
            raise typer.Exit(self.format_error(msg))  # type: ignore

    def format_error(self, msg: str) -> str:
        _msg = "[ERROR]"
        if cls := self.klass:
            _msg += f" in class {cls}"
        if fn := self.function:
            _msg += f" in function {fn}"
        if cs := self.context_start:
            _msg += f" starting at line {cs}"
        if sf := self.source_file:
            _msg += f" in {sf}"
        return _msg + ":\n" + msg

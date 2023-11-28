#: util.py
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import typer


def separator(id: str, sep_char: str = "-") -> str:
    BEGIN = 5
    WIDTH = 50
    start = f"{sep_char * BEGIN} {id} "
    return start + f"{(WIDTH - len(start)) * sep_char}" + "\n"


@dataclass
class ErrorReporter:
    file_path: Path
    current_line_number: Optional[int] = None

    def assert_true(self, condition: bool, msg: str) -> None:
        if not condition:
            raise typer.Exit(self.format_error_message(msg))  # type: ignore

    def format_error_message(self, msg: str) -> str:
        error_location = (
            f'File "{self.file_path}", Line {self.current_line_number}: '
            if self.current_line_number
            else f'File "{self.file_path}": '
        )
        return error_location + msg

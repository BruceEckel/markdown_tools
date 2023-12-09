"Prompt responding to a single character, without carriage return"
import readchar
from markdown_tools.console import console
from rich.panel import Panel, Text
from rich import box


def prompt(
    msg: str = "",
) -> bool:
    _prompt = "'y' -> make change (otherwise skip)"
    if msg:
        _prompt += f": {msg}"
    console.print(
        Panel(
            Text(_prompt, style="orange1"),
            box=box.DOUBLE,
            border_style="red3",
            expand=False,
        ),
    )
    # Read a keypress, no CR needed.
    # Can also capture arrows etc:
    response = readchar.readkey()
    if response == "y":
        return True
    return False


# Demo
if __name__ == "__main__":
    for n in range(10):
        r = prompt(str(n))
        if r is True:
            break

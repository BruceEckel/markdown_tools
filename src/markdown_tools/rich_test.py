from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table
from rich.markdown import Markdown
from rich.rule import Rule

MARKDOWN = """
# This is an h1

Rich can do a pretty *decent* job of rendering markdown.

1. This is a list item
2. This is another list item
"""

console = Console()
md = Markdown(MARKDOWN)
console.print(md)

r = Rule("foo")
console.print(r)


class Bob:
    def __rich__(self):
        return Rule("Bob")


b = Bob()
console.print(b)


@dataclass
class Student:
    id: int
    name: str
    age: int

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield Rule(f"[b]Student:[/b] #{self.id}")
        my_table = Table("Attribute", "Value")
        my_table.add_row("name", self.name)
        my_table.add_row("age", str(self.age))
        yield my_table


s = Student(99, "Bob Dobbs", 22)
console.print(s)

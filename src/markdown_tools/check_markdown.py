#: check_markdown.py
from io import StringIO
from pathlib import Path
import typer
from markdown_tools import MarkdownFile


def check_markdown(md: Path):
    markdown = MarkdownFile(md)
    for code_path in markdown.code_paths():
        print(f"\npath: {code_path.path}")

    # Regenerate markdown file into memory:
    new_markdown = StringIO()
    new_markdown.write(
        "".join([repr(section) for section in markdown])
    )
    new_markdown.seek(0)
    # Compare regenerated file to file on disk:
    if new_markdown.read() == md.read_text(encoding="utf-8"):
        return "OK"
    else:
        # Create comparison file:
        Path(md.name + ".mtmp").write_text(
            "".join([repr(section) for section in markdown]),
            encoding="utf-8",
        )
        raise typer.Exit(
            f"\nERROR: Regenerated file '{md.name}.mtmp'\n"  # type: ignore
            + f"is not the same as original '{md.name}'\n"
        )

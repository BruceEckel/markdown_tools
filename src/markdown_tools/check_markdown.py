#: check_markdown.py
from io import StringIO
from pathlib import Path
from .markdown_file import MarkdownFile
from .error_reporter import check
from .console import console


def check_markdown(md: Path):
    markdown = MarkdownFile(md)
    for code_path in markdown.code_paths():
        console.print(f"\npath: {code_path.path}")
    # Regenerate markdown file into memory:
    new_markdown = StringIO()
    new_markdown.write(
        "".join([repr(section) for section in markdown])
    )
    new_markdown.seek(0)
    # Compare regenerated file to file on disk:
    if new_markdown.read() == md.read_text(encoding="utf-8"):
        return "[green bold][OK][/green bold]"
    else:
        comparison_file_path = markdown.file_path.with_suffix(
            ".tmp.md"
        )
        markdown.write_new_file(comparison_file_path)
        check.error(
            f"Regenerated file '{comparison_file_path.name}'\n"
            + f"is not the same as original '{md.name}'\n"
        )

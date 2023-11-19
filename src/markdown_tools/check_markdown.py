# check_markdown.py
from io import StringIO
from pathlib import Path
from .markdown_file import MarkdownFile


def check_markdown(md: Path):
    markdown = MarkdownFile(md)
    for ghurl in markdown.github_urls():
        print(f"GitHubURL: {ghurl.url}")
    new_markdown = StringIO()
    new_markdown.write(
        "".join([repr(section) for section in markdown])
    )
    new_markdown.seek(0)
    if new_markdown.read() == md.read_text(encoding="utf-8"):
        return "OK"
    else:
        Path(md.name + ".mtmp").write_text(
            "".join([repr(section) for section in markdown]),
            encoding="utf-8",
        )
        return "Not the same"

# test_markdown_file.py
import pytest
from markdown_tools import (
    separator,
    MarkdownBlock,
    SourceCodeListing,
    CodePath,
    MarkdownFile,
)
from pathlib import Path


# Tests for MarkdownText
def test_markdown_text_repr():
    text = MarkdownBlock("Example text")
    assert repr(text) == "Example text"


def test_markdown_text_str():
    text = MarkdownBlock("Example text")
    assert "MarkdownText" in str(text)
    assert "Example text" in str(text)


# Tests for SourceCodeListing
def test_source_code_listing_python():
    code_block = (
        "```python\n# example.py\nprint('Hello, world!')\n```"
    )
    listing = SourceCodeListing(code_block)
    assert listing.language == "python"
    assert listing.source_file_name == "example.py"
    assert "Hello, world!" in listing.code


# Add more tests for different languages and edge cases


# Tests for GitHubURL
def test_github_url_repr():
    url = CodePath("https://github.com/example/repo")
    assert (
        repr(url) == "%%\ncode: https://github.com/example/repo\n%%\n"
    )


# Tests for MarkdownFile
def test_markdown_file_parsing():
    markdown_content = (
        "Normal text\n"
        "```python\n# example.py\nprint('Hello, world!')\n```\n"
        "%%\ncode: https://github.com/example/repo\n%%\n"
    )
    file_path = Path("test.md")
    file_path.write_text(markdown_content)
    markdown_file = MarkdownFile(file_path)

    assert len(markdown_file.contents) == 3
    assert isinstance(markdown_file.contents[0], MarkdownBlock)
    assert isinstance(markdown_file.contents[1], SourceCodeListing)
    assert isinstance(markdown_file.contents[2], CodePath)

    # Cleanup
    file_path.unlink()


# Add more tests to cover other scenarios and edge cases

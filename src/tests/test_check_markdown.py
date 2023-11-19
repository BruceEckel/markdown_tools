import pytest
from pathlib import Path
from io import StringIO
from unittest.mock import patch
from markdown_tools.check_markdown import check_markdown
from markdown_tools.markdown_file import MarkdownFile


@pytest.fixture
def create_test_file(tmp_path):
    def _create_test_file(contents, file_name="test.md"):
        p = tmp_path / file_name
        p.write_text(contents, encoding="utf-8")
        return p

    return _create_test_file


def test_check_markdown_with_github_url(create_test_file):
    md_content = "%%\ncode: https://github.com/example/repo\n%%\n"
    md_path = create_test_file(md_content)

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        assert check_markdown(md_path) == "OK"
        assert (
            "GitHubURL: https://github.com/example/repo"
            in mock_stdout.getvalue()
        )


def test_check_markdown_identical_content(create_test_file):
    md_content = "# Sample Markdown\n\nThis is a test."
    md_path = create_test_file(md_content)
    assert check_markdown(md_path) == "OK"


def test_check_markdown_different_content(create_test_file):
    md_content = "# Sample Markdown\n\nThis is a test."
    md_modified_content = (
        "# Sample Markdown\n\nThis is a modified test."
    )
    md_path = create_test_file(md_content)
    md_path.write_text(md_modified_content, encoding="utf-8")

    assert check_markdown(md_path) == "Not the same"
    assert (md_path.parent / (md_path.name + ".mtmp")).read_text(
        encoding="utf-8"
    ) == md_modified_content


# Additional tests can be written to cover more scenarios and edge cases.

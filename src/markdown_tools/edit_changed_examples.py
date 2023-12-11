# edit_changed_examples.py
"""
Creates and updates file_edit_script which opens files with content
differences inside VSCode.
"""
from pathlib import Path
from markdown_tools.markdown_file import (
    MarkdownFile,
    SourceCode,
    check,
)
from markdown_tools.compare_strings import compare_strings, DiffResult
from markdown_tools.vscode_open import vscode_open


def edit_example_changes(md: Path, file_edit_script: Path) -> None:
    md_file = MarkdownFile(md)
    md_file.display_name_once()
    for (
        code_path,
        example_code,
    ) in md_file.code_path_and_example_code():
        full_path = Path(code_path.path) / Path(  # type: ignore
            example_code.source_file_name
        )
        check.is_true(
            full_path.exists(),
            f"{full_path.as_posix()} does not exist",
        )
        source_file = SourceCode.from_source_file(full_path)
        diff = compare_strings(example_code.code, source_file.code)
        diff.show_result(full_path)
        if diff.result == DiffResult.CONTENT:
            vscode_open(file_edit_script, full_path)

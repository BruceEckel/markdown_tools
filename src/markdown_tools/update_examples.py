# update_listings.py
from pathlib import Path
from markdown_tools.markdown_file import (
    MarkdownFile,
    SourceCode,
    check,
)
from markdown_tools.utils import prompt
from markdown_tools.console import console
from markdown_tools.compare_strings import compare_strings, DiffResult


def update_examples_from_source_code(md: Path) -> None:
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

        def prompt_and_update():
            diff.show_diffs(md_file)
            if prompt():
                console.print(
                    "Replacing markdown example with source file"
                )
                md_file[md_file.index_of(example_code)] = source_file
                md_file.update()
            else:
                console.print(
                    f"No changes to {example_code.source_file_name}"
                )

        match diff.result:
            case DiffResult.NONE:
                assert source_file == example_code
            case DiffResult.BLANK_LINES:
                prompt_and_update()
            case DiffResult.CONTENT:
                prompt_and_update()

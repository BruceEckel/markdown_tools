#: markdown_file.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, List
import typer


def separator(id: str, sep_char: str = "-") -> str:
    BEGIN = 5
    WIDTH = 50
    start = f"{sep_char * BEGIN} {id}"
    return start + f" {(WIDTH - len(start)) * sep_char}" + "\n"


def assert_true(condition: bool, msg: str):
    if not condition:
        raise typer.Exit(msg)  # type: ignore


@dataclass
class MarkdownSourceText:
    """
    Delivers the markdown file a line at a time.
    Keeps track of the current line.
    Knows the Path of the file, for use in error messages.
    """

    file_path: Path
    original_markdown: str = ""
    lines: List[str] = field(default_factory=list)
    current_line_number: int = 0
    start_of_block: int = 0  # For error messages

    def _assert_true(self, condition: bool, msg: str):
        assert_true(condition, f"ERROR in {self.file_path}: " + msg)

    def __post_init__(self):
        self._assert_true(self.file_path.exists(), "does not exist")
        self._assert_true(
            not self.file_path.is_dir(), "is a directory"
        )
        self._assert_true(
            self.file_path.suffix == ".md", "does not end with '.md'"
        )
        self.original_markdown = self.file_path.read_text(
            encoding="utf-8"
        )
        self.lines = self.original_markdown.splitlines(True)

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.current_line_number >= len(self.lines):
            raise StopIteration
        line = self.lines[self.current_line_number]
        self.current_line_number += 1
        return line

    def __bool__(self) -> bool:
        return self.current_line_number < len(self.lines)

    def current_line(self) -> str | None:
        """
        Produce the current line.
        """
        if self.current_line_number >= len(self.lines):
            return None
        return self.lines[self.current_line_number]

    def assert_true(self, condition: bool, msg: str):
        start_err = f" at line {self.start_of_block}:\n"
        self._assert_true(condition, start_err + msg)


@dataclass
class MarkdownBlock:
    """
    Contains a section of normal markdown text
    """

    md_source: MarkdownSourceText
    text: str

    def __repr__(self) -> str:
        return f"{self.text}"

    def __str__(self) -> str:
        return separator("MarkdownText") + repr(self)

    @staticmethod
    def parse(
        md_source: MarkdownSourceText,
    ) -> "MarkdownBlock":
        # We know the current line is good:
        text_lines = [next(md_source)]

        while md_source.current_line():
            if md_source.current_line().startswith(
                "```"
            ) or md_source.current_line().startswith("%%"):
                break
            text_lines.append(next(md_source))

        return MarkdownBlock(md_source, "".join(text_lines))


@dataclass
class SourceCodeListing:
    """
    Contains a single source-code listing:
    A.  All listings begin and end with ``` markers.
    B.  Programming-language listings use ``` followed
        immediately by the name of the language (no space!)
    C.  If it is program output, the name of the language is `text`.
    D.  Providing no language name is not allowed.
    E.  A `!` after the language name tells the program
        to allow no slug-line, for code fragments that don't have
        an associated file.
    """

    original_code_block: str
    language: str = ""
    source_file_name: str = ""
    code: str = ""
    ignore: bool = False

    def __post_init__(self):
        lines = self.original_code_block.splitlines(True)
        tagline = lines[0].strip()
        filename_line = lines[1].strip() if len(lines) > 1 else ""

        self.ignore = tagline.endswith("!")
        tagline = tagline.rstrip("!")
        self.language = tagline[3:].strip()
        self.code = "".join(lines[1:-1])

        assert_true(
            self.language,
            f"Language cannot be empty in {self.original_code_block}",
        )

        if self.ignore:
            return

        match self.language:
            case "python":
                self._validate_filename(filename_line, "#", ".py")
            case "rust":
                self._validate_filename(filename_line, "//", ".rs")
            case "go":
                self._validate_filename(filename_line, "//", ".go")
            case "text":
                pass

    def _validate_filename(
        self, line: str, comment: str, file_ext: str
    ):
        assert line.startswith(comment) and line.endswith(
            file_ext
        ), f"First line must contain source file name in {self.original_code_block}"
        self.source_file_name = line[len(comment) :].strip()

    @staticmethod
    def parse(
        md_source: MarkdownSourceText,
    ) -> "SourceCodeListing":
        code_lines: List[str] = [next(md_source)]

        def _assert_true(condition: bool):
            assert_true(
                condition,
                f"Unclosed code block starting at line {md_source.start_of_block}",
            )

        while (
            md_source.current_line()
            and md_source.current_line().strip() != "```"
        ):
            # Means there's more on the line after the ```:
            _assert_true(
                not md_source.current_line().startswith("```")
            )
            code_lines.append(next(md_source))

        code_lines.append(next(md_source))  # Include closing ```
        return SourceCodeListing("".join(code_lines))

    def __repr__(self) -> str:
        def ignore_marker():
            return " !" if self.ignore else ""

        return (
            f"```{self.language}{ignore_marker()}\n"
            + "".join(self.code)
            + "```\n"
        )

    def __str__(self) -> str:
        return (
            separator("SourceCodeListing")
            + repr(self)
            + f"{self.source_file_name = }\n"
            + f"{self.language = } {self.ignore = }"
        )


@dataclass
class CodePath:
    """
    Contains a path to a directory containing code files.
    Represented in the markdown file as:
    %%
    path: directory
    %%
    Each one of these sets the directory for subsequent code listings.
    """

    md_source: MarkdownSourceText
    comment: List[str]
    path: str | None = None

    def __post_init__(self):
        self.md_source.assert_true(
            self.comment[1].startswith("path:"),
            f"Missing 'path:' in:\n{self}",
        )
        self.path = self.comment[1].lstrip("path:").strip()

    def __repr__(self) -> str:
        return f"%%\n{self.comment[1]}\n%%\n"

    def __str__(self) -> str:
        return "\n" + separator("CodePath") + repr(self)

    @staticmethod
    def parse(
        md_source: MarkdownSourceText,
    ) -> "CodePath":
        comment: List[str] = [next(md_source).rstrip()]  # Initial %%
        while True:
            comment.append(next(md_source).rstrip())
            if comment[-1] == "%%":  # Closing comment marker
                break
            md_source.assert_true(
                md_source.current_line(), "Unclosed markdown comment"
            )

        return CodePath(md_source, comment)


@dataclass
class MarkdownFile:
    file_path: Path
    md_source: MarkdownSourceText
    contents: List[MarkdownBlock | SourceCodeListing | CodePath]

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.md_source = MarkdownSourceText(self.file_path)
        self.contents = list(MarkdownFile.parse(self.md_source))

    @staticmethod
    def parse(
        markdown_source: MarkdownSourceText,
    ) -> Iterator[MarkdownBlock | SourceCodeListing | CodePath]:
        while current_line := markdown_source.current_line():
            if current_line.startswith("```"):
                yield SourceCodeListing.parse(markdown_source)
            elif current_line.startswith("%%"):
                yield CodePath.parse(markdown_source)
            else:
                yield MarkdownBlock.parse(markdown_source)

    def __iter__(
        self,
    ) -> Iterator[MarkdownBlock | SourceCodeListing | CodePath]:
        return iter(self.contents)

    def code_listings(self) -> List[SourceCodeListing]:
        return [
            part
            for part in self
            if isinstance(part, SourceCodeListing)
        ]

    def code_paths(self) -> List[CodePath]:
        return [part for part in self if isinstance(part, CodePath)]

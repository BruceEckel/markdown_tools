#: markdown_file.py
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Tuple
import typer


def separator(id: str, sep_char: str = "-") -> str:
    BEGIN = 5
    WIDTH = 50
    start = f"{sep_char * BEGIN} {id}"
    return start + f" {(WIDTH - len(start)) * sep_char}" + "\n"


def abort(condition: bool, msg: str):
    if condition:
        raise typer.Exit(msg)  # type: ignore


@dataclass
class MarkdownText:
    """
    Contains a section of normal markdown text
    """

    text: str

    def __repr__(self) -> str:
        return f"{self.text}"

    def __str__(self) -> str:
        return separator("MarkdownText") + repr(self)

    @staticmethod
    def parse(
        source: List[str], start_line: int
    ) -> Tuple["MarkdownText", int]:
        text_lines = []
        line_number = start_line

        while (
            line_number < len(source)
            and not source[line_number].startswith("```")
            and source[line_number].strip() != "%%"
        ):
            text_lines.append(source[line_number])
            line_number += 1

        return MarkdownText("".join(text_lines)), line_number


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

        assert (
            self.language
        ), f"Language cannot be empty in {self.original_code_block}"

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

    @staticmethod
    def parse(
        source: List[str], start_line: int
    ) -> Tuple["SourceCodeListing", int]:
        code_lines: List[str] = [source[start_line]]
        line_number: int = start_line + 1

        def _abort(condition: bool):
            abort(
                condition,
                f"Unclosed code block starting at line {start_line}",
            )

        while (
            line_number < len(source)
            and source[line_number].strip() != "```"
        ):
            # Means there's more after the ```:
            _abort(source[line_number].startswith("```"))
            code_lines.append(source[line_number])
            line_number += 1

        _abort(line_number >= len(source))
        code_lines.append(source[line_number])  # Include closing ```
        return SourceCodeListing("".join(code_lines)), line_number + 1

    def _validate_filename(
        self, line: str, comment: str, file_ext: str
    ):
        assert line.startswith(comment) and line.endswith(
            file_ext
        ), f"First line must contain source file name in {self.original_code_block}"
        self.source_file_name = line[len(comment) :].strip()

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

    comment: List[str]
    start_line: int
    path: str | None = None

    def __post_init__(self):
        if not self.comment[1].startswith("path:"):
            raise typer.Exit(
                f"\nError: line {self.start_line}\nMissing 'path:' in:\n{self}"
            )
        self.path = self.comment[1].lstrip("path:").strip()

    def __repr__(self) -> str:
        return f"%%\n{self.comment[1]}\n%%\n"

    def __str__(self) -> str:
        return "\n" + separator("CodePath") + repr(self)

    @staticmethod
    def parse(
        source: List[str], start_line: int
    ) -> Tuple["CodePath", int]:
        comment: List[str] = [source[start_line].rstrip()]
        line_n = start_line + 1
        while True:
            comment.append(source[line_n].rstrip())
            line_n += 1
            if comment[-1] == "%%":
                break

        return CodePath(comment, start_line), line_n


@dataclass
class MDSourceText:
    """
    Delivers the markdown file a line at a time.
    Keeps track of the current line.
    Knows the Path of the file, for use in error messages.
    """

    file_path: Path
    original_markdown: str = ""
    lines: List[str] | None = None
    current_line: int = 0

    def __post_init__(self):
        abort(
            not self.file_path.exists(),
            f"ERROR: [{self.file_path}] does not exist",
        )
        abort(
            self.file_path.is_dir(),
            f"ERROR: [{self.file_path}] is a directory",
        )
        abort(
            self.file_path.suffix != ".md",
            f"ERROR: [{self.file_path}] does not end with '.md'",
        )
        self.original_markdown = self.file_path.read_text(
            encoding="utf-8"
        )
        self.lines = self.original_markdown.splitlines(True)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_line >= len(self.lines):
            raise StopIteration
        line = self.lines[self.current_line]
        self.current_line += 1
        return line


@dataclass
class MarkdownFile:
    original_markdown: str
    contents: List[MarkdownText | SourceCodeListing | CodePath]

    def __init__(self, file_path: Path):
        self.original_markdown = file_path.read_text(encoding="utf-8")
        self.contents = list(
            MarkdownFile.parse(
                self.original_markdown.splitlines(True)
            )
        )

    @staticmethod
    def parse(
        source: List[str],
    ) -> Iterator[MarkdownText | SourceCodeListing | CodePath]:
        line_number = 0

        while line_number < len(source):
            line = source[line_number]

            if line.startswith("```"):
                listing, line_number = SourceCodeListing.parse(
                    source, line_number
                )
                yield listing
            elif line.strip() == "%%":
                code_path, line_number = CodePath.parse(
                    source, line_number
                )
                yield code_path
            else:
                markdown_text, line_number = MarkdownText.parse(
                    source, line_number
                )
                yield markdown_text

    def __iter__(
        self,
    ) -> Iterator[MarkdownText | SourceCodeListing | CodePath]:
        return iter(self.contents)

    def code_listings(self) -> List[SourceCodeListing]:
        return [
            part
            for part in self
            if isinstance(part, SourceCodeListing)
        ]

    def code_paths(self) -> List[CodePath]:
        return [part for part in self if isinstance(part, CodePath)]

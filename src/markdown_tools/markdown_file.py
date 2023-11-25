#: markdown_file.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, List, Union, TypeAlias
import typer


def separator(id: str, sep_char: str = "-") -> str:
    BEGIN = 5
    WIDTH = 50
    start = f"{sep_char * BEGIN} {id} "
    return start + f"{(WIDTH - len(start)) * sep_char}" + "\n"


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

    def _assert_true(self, condition: bool, msg: str) -> None:
        if not condition:
            raise typer.Exit(f"ERROR [{self.file_path}] " + msg)  # type: ignore

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
        Produce the current line or None if past the end.
        Does not increment current_line_number like next() does.
        """
        if self.current_line_number >= len(self.lines):
            return None
        return self.lines[self.current_line_number]

    def assert_true(self, condition: bool, msg: str):
        start_err = f" at line {self.start_of_block}:\n"
        self._assert_true(condition, start_err + msg)


@dataclass
class Markdown:
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
    ) -> "Markdown":
        # We know the current line is good:
        text_lines = [next(md_source)]

        while line := md_source.current_line():
            if line.startswith("```") or line.startswith("%%"):
                break
            text_lines.append(next(md_source))

        return Markdown(md_source, "".join(text_lines))


@dataclass
class SourceCode:
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
    md_source: MarkdownSourceText
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

        self.md_source.assert_true(
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
    ) -> "SourceCode":
        code_lines: List[str] = [next(md_source)]

        while line := md_source.current_line():
            code_lines.append(next(md_source))  # Include closing ```
            if line.startswith("```"):
                # Closing tag must not be followed by a language:
                md_source.assert_true(
                    len(line.strip()) == len("```"),
                    "Unclosed code block",
                )
                break

        return SourceCode("".join(code_lines), md_source)

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
            separator("SourceCode")
            + repr(self)
            + f"{self.source_file_name = }\n"
            + f"{self.language = } {self.ignore = }"
        )


@dataclass
class Comment:
    """
    Our special Markdown comments that use the following format:
    %%
    Yawn boring stuff that doesn't concern us
    %%
    Unless the special comment contains information we're
    looking for, this is just a placeholder to hold the comment.
    Markdown comments that do not follow the above format
    are just passed through the parser unnoticed. Thus we
    only allow/look for start & end marker lines that are
    *exactly* `%%`
    """

    md_source: MarkdownSourceText
    comment: List[str]

    def __repr__(self) -> str:
        return "".join(self.comment)

    def __str__(self) -> str:
        return "\n" + separator("Comment") + repr(self)

    # Indexing including slicing:
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.comment[index.start : index.stop : index.step]
        return self.comment[index]

    def __iter__(self):
        return iter(self.comment)

    @staticmethod
    def parse(
        md_source: MarkdownSourceText,
    ) -> Union["Comment", "CodePath"]:
        comment: List[str] = [next(md_source)]  # Initial %%
        while True:
            comment.append(next(md_source))
            if comment[-1].rstrip() == "%%":  # Closing comment marker
                break
            md_source.assert_true(
                bool(md_source.current_line()),
                "Unclosed markdown comment",
            )
        batch = "".join(comment)
        if "url:" in batch or "path:" in batch:
            return CodePath(Comment(md_source, comment))

        return Comment(md_source, comment)


@dataclass
class CodePath:
    """
    A special comment containing a path to a directory of code files.
    Each of these resets the directory for subsequent code listings.
    Represented in the markdown file as:
    %%
    path: directory
    url: URL
    %%
    There must be at least one of "path:" or "url:" or the comment
    will be ignored (i.e. an ordinary `Comment`).
    """

    comment: Comment
    path: str | None = None
    url: str | None = None

    def __post_init__(self):
        def exists(id: str) -> bool:
            return self.comment[1].startswith(id)

        self.comment.md_source.assert_true(
            exists("path:") or exists("url:"),
            f"Missing 'path:' or 'url:' in:\n{self}",
        )
        for line in self.comment:
            if line.startswith("path:"):
                self.path = line.strip("path:").strip()
            if line.startswith("url:"):
                self.url = line.strip("url:").strip()

    def validate(self, tail_path: str) -> Path | None:
        assert self.path, f"Cannot validate empty path in:\n{self}"
        start = Path(self.path)
        assert (
            start.exists()
        ), f"Starting path {start.as_posix()} does not exist"
        for file in start.rglob(tail_path):
            return file
        return None

    @staticmethod
    def new(md_file: "MarkdownFile", path: Path):
        "Create a CodePath from Path"
        md_file.md_source.assert_true(
            path.exists(), f"{path} doesn't exist"
        )
        comment: List[str] = [
            "%%\n",
            f"path: {path.as_posix()}\n",
            "%%\n",
        ]
        return CodePath(Comment(md_file.md_source, comment))

    def __repr__(self) -> str:
        return repr(self.comment)

    def __str__(self) -> str:
        return (
            "\n"
            + separator("CodePath")
            + f"path: [{self.path}]\n"
            + f"url: [{self.url}]\n"
            + repr(self)
        )


MarkdownPart: TypeAlias = Markdown | SourceCode | CodePath | Comment


@dataclass
class MarkdownFile:
    file_path: Path
    md_source: MarkdownSourceText
    contents: List[MarkdownPart]
    name_already_displayed: bool = False

    def __init__(self, file_path: Path):
        assert file_path.exists()
        assert file_path.is_file()
        self.file_path = file_path
        self.md_source = MarkdownSourceText(self.file_path)
        self.contents = list(MarkdownFile.parse(self.md_source))

    def display_name_once(self, end=""):
        if self.name_already_displayed:
            return
        self.name_already_displayed = True
        print(separator(self.file_path.name, "-"), end=end)

    @staticmethod
    def parse(
        md_source: MarkdownSourceText,
    ) -> Iterator[MarkdownPart]:
        while current_line := md_source.current_line():
            match current_line:
                case line if line.startswith("```"):
                    yield SourceCode.parse(md_source)
                case line if line.strip() == "%%":
                    yield Comment.parse(md_source)
                case _:
                    yield Markdown.parse(md_source)

    def write_new_file(self, file_path: Path):
        # assert not file_path.exists()
        file_path.write_text(
            "".join([repr(section) for section in self.contents]),
            encoding="utf-8",
        )

    def __contains__(self, item: MarkdownPart) -> bool:
        result = [
            part for part in self.contents if isinstance(part, item)
        ]
        # print(f"__contains__({self.file_path}, {item}): {result}")
        return result

    def __getitem__(self, index: int):
        if isinstance(index, slice):
            return self.contents[
                index.start : index.stop : index.step
            ]
        return self.contents[index]

    def __setitem__(self, index, value: MarkdownPart):
        self.contents[index] = value

    def __len__(self):
        return len(self.contents)

    def index_of(self, item):
        try:
            return self.contents.index(item)
        except ValueError:
            return -1

    def insert(self, index, item):
        self.contents.insert(index, item)

    def __iter__(
        self,
    ) -> Iterator[MarkdownPart]:
        return iter(self.contents)

    def code_listings(self) -> List[SourceCode]:
        return [part for part in self if isinstance(part, SourceCode)]

    def pathed_code_listings(self) -> List[SourceCode]:
        # Any code listings that are not explicitly ignored
        return [
            part
            for part in self.code_listings()
            if not part.language == "text" and not part.ignore
        ]

    def code_paths(self) -> List[CodePath]:
        return [part for part in self if isinstance(part, CodePath)]

    def codepaths_exist(self) -> bool:
        if not self.pathed_code_listings():
            return False  # No CodePaths needed
        if self.code_paths():
            return False  # Already exists (TODO: might be url: and not :path)
        return True

    def comments(self) -> List[Comment | CodePath]:
        return [
            part
            for part in self
            if isinstance(part, Comment) or isinstance(part, CodePath)
        ]

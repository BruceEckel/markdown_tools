#: languages.py
"""
Look up language information using either the language name or
the code file extension.
"""
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageInfo:
    language: str
    file_extension: str
    comment_symbol: str
    start_search: str


_languages: List[LanguageInfo] = [
    LanguageInfo("python", ".py", "#", "C:/git/python-experiments"),
    LanguageInfo("rust", ".rs", "//", "C:/git/rust-experiments"),
    LanguageInfo("go", ".go", "//", "C:/git/go-experiments"),
]


class LanguageMeta(type):
    # Subscripting & 'in' for the Language class

    def __getitem__(cls, key: str):
        for language_info in cls._code_types:  # type:ignore
            if (
                language_info.language == key
                or language_info.file_extension == key
            ):
                return language_info
        raise KeyError(f"No LanguageInfo found for key: {key}")

    def __contains__(cls, key: str) -> bool:
        return any(
            key in (lang.language, lang.file_extension)
            for lang in cls._code_types  # type:ignore
        )


class Languages(metaclass=LanguageMeta):
    _code_types: List[LanguageInfo] = _languages


if __name__ == "__main__":
    print(Languages["python"])
    print(Languages[".py"])
    print("python" in Languages)
    print(".py" in Languages)

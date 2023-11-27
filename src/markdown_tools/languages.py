#: languages.py
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageInfo:
    language: str
    file_extension: str
    comment_symbol: str
    start_search: str


code_types: List[LanguageInfo] = [
    LanguageInfo("python", ".py", "#", "C:/git/python-experiments"),
    LanguageInfo("rust", ".rs", "//", "C:/git/rust-experiments"),
    LanguageInfo("go", ".go", "//", "C:/git/go-experiments"),
]


class LanguageMeta(type):
    # Provide subscripting & 'in' for the Language class

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


class Language(metaclass=LanguageMeta):
    _code_types: List[LanguageInfo] = code_types


if __name__ == "__main__":
    print(Language["python"])
    print(Language[".py"])
    print("python" in Language)
    print(".py" in Language)

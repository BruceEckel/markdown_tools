#: languages.py
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageInfo:
    language: str
    file_extension: str
    comment_symbol: str
    start_search: str
    source_file_name_required: bool = True


_languages: List[LanguageInfo] = [
    LanguageInfo("python", ".py", "#", "C:/git/python-experiments"),
    LanguageInfo("rust", ".rs", "//", "C:/git/rust-experiments"),
    LanguageInfo("go", ".go", "//", "C:/git/go-experiments"),
    LanguageInfo("text", ".txt", "", "", False),
]


@dataclass(frozen=True)
class Languages:
    _languages: List[LanguageInfo]

    def __getitem__(self, key: str) -> LanguageInfo:
        for language_info in self._languages:
            if (
                key == language_info.language
                or key == language_info.file_extension
            ):
                return language_info
        raise KeyError(f"No LanguageInfo found for key: {key}")

    def __contains__(self, key: str) -> bool:
        return any(
            key in (lang.language, lang.file_extension)
            for lang in self._languages
        )


LANGUAGES = Languages(_languages)  # Singleton

if __name__ == "__main__":
    print(LANGUAGES["python"])  # Using language name
    print(LANGUAGES[".py"])  # Using file extension
    print("python" in LANGUAGES)
    print(".py" in LANGUAGES)

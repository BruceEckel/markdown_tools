#: languages.py
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


class Languages:
    def __init__(self, languages: List[LanguageInfo]):
        self._languages = languages

    def __getitem__(self, key: str) -> LanguageInfo:
        for language_info in self._languages:
            if (
                language_info.language == key
                or language_info.file_extension == key
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

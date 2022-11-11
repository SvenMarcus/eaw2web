from typing import Iterable, TypeGuard
from eaw2web.typing import Pair


def _parse_to_text_dict(path: str):
    def is_pair(_tuple: tuple[str, ...]) -> TypeGuard[Pair[str, str]]:
        return len(_tuple) == 2

    with open(path, mode="r") as f:
        kv_pairs = filter(is_pair, [from_csv_line(line, maxsplit=1) for line in f])
        return dict(kv_pairs)


def _parse_all_text_files(files: list[str]) -> dict[str, str]:
    text_dict: dict[str, str] = {}
    for csv in files:
        text_dict.update(_parse_to_text_dict(csv))

    return text_dict


def bool_from_str(string: str | None) -> bool:
    return string is not None and string.lower() in ("true", "yes")


def from_csv_line(line: str, *, maxsplit: int = -1) -> tuple[str, ...]:
    return tuple(line.strip().split(",", maxsplit=maxsplit))


def preserve_newlines(text: str) -> str:
    return text.replace("\\n", "\n")


def strip_entries(split_text: Iterable[str]) -> list[str]:
    return [entry.strip() for entry in split_text]


class Encyclopedia(dict[str, str]):
    def __init__(self, text_files: list[str]) -> None:
        super().__init__(_parse_all_text_files(text_files))
        self.text_files = text_files

    def get_text(self, text_id: str) -> str:
        cleaned_text_content = text_id.upper().strip()
        return self.get(cleaned_text_content, "")

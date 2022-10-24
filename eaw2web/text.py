from xml.etree.ElementTree import Element


def text_entry_for_string(string: str, text_dict: dict[str, str]):
    cleaned_text_content = string.upper().strip()
    if cleaned_text_content not in text_dict:
        return ""

    return text_dict[cleaned_text_content]


def text_entry_from_tag(tag: Element, text_dict: dict[str, str]):
    if tag is not None and tag.text is not None:
        return text_entry_for_string(tag.text, text_dict)

    return ""


def collect_tooltips(child: Element, text_dict: dict[str, str]) -> list[str]:
    tooltips_tag = child.find("Encyclopedia_Text")
    if tooltips_tag is None:
        return []

    if tooltips_tag.text is None:
        return []

    clean_text_content = tooltips_tag.text.strip()
    return [text_dict.get(tt, "") for tt in clean_text_content.split()]


def parse_to_text_dict(path: str):
    text_dict: dict[str, str] = dict()
    with open(path, mode="r") as f:
        line: str
        for line in f:
            t = tuple(line.strip().split(",", maxsplit=1))
            text_dict[t[0]] = t[1]

    return text_dict


class Encyclopedia(dict[str, str]):
    def __init__(self, text_files: list[str]) -> None:
        super().__init__(self._parse_all_text_files(text_files))
        self.text_files = text_files

    def _parse_all_text_files(self, files: list[str]) -> dict[str, str]:
        text_dict: dict[str, str] = {}
        for csv in files:
            text_dict.update(parse_to_text_dict(csv))

        return text_dict

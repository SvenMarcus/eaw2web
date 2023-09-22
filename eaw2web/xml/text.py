from typing import Iterable, Optional
from xml.etree.ElementTree import Element


def collect_texts(elements: Iterable[Element]) -> list[str]:
    return [element.text.strip() for element in elements if element.text]


def text_or_empty(tag: Optional[Element]) -> str:
    if tag is None:
        return ""

    return (tag.text or "").strip()

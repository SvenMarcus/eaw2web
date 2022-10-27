from typing import Optional
from xml.etree.ElementTree import Element

from eaw2web.text import Encyclopedia


def text_entry_from_tag(tag: Optional[Element], text_dict: Encyclopedia):
    return text_dict.get_text(text_or_empty(tag))


def text_or_empty(tag: Optional[Element]) -> str:
    if tag is None:
        return ""

    return (tag.text or "").strip()


def collect_tooltips(child: Element, text_dict: Encyclopedia) -> list[str]:
    tooltips_tag = child.find("Encyclopedia_Text")
    if tooltips_tag is None:
        return []

    if tooltips_tag.text is None:
        return []

    clean_text_content = tooltips_tag.text.strip()
    return [text_dict.get_text(tt) for tt in clean_text_content.split()]

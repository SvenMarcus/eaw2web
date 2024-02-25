from typing import Optional
from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import TextEntry
from eaw2web.xml.tags import TagParser, allow_missing
from eaw2web.xml.text import text_or_empty
from eaw2web.text import Encyclopedia


def collect_tooltips(parser: TagParser, text_dict: Encyclopedia) -> list[TextEntry]:
    text = allow_missing(parser.text, "Encyclopedia_Text", fallback="")

    clean_text_content = text.strip()
    return [text_dict.get_text(tt) for tt in clean_text_content.split()]


def text_entry_from_tag(tag: Optional[Element], text_dict: Encyclopedia) -> TextEntry:
    return text_dict.get_text(text_or_empty(tag))

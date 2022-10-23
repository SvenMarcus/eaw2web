from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import Unit
from eaw2web.xml.generic import parse_generic_game_object
from eaw2web.xml.icon import icon_name
from eaw2web.text import collect_tooltips


def parse_unit_object(child: Element, text_dict: dict[str, str]):
    return Unit(
        **parse_generic_game_object(child, text_dict).dict(),
        icon=icon_name(child),
        tooltips=collect_tooltips(child, text_dict),
        affiliation=affiliation(child),
        tech_level=text_or_empty(child, "Tech_Level"),
    )


def affiliation(child: Element):
    affiliation_text = text_or_empty(child, "Affiliation")
    split_affiliation = affiliation_text.split(",")
    return [
        affiliation.strip() for affiliation in split_affiliation if affiliation.strip()
    ]


def text_or_empty(child: Element, tag_name: str):
    tag = child.find(tag_name)
    if tag is None:
        return ""

    return tag.text or ""

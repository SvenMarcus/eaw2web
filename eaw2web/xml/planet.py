from xml.etree import ElementTree as et

from eaw2web.gameobjecttypes import Planet
from eaw2web.xml.generic import parse_generic_game_object, text_entry_from_tag

DESCRIPTION_TAGS = [
    "Describe_History",
    "Describe_Population",
    "Describe_Wildlife",
    "Describe_Terrain",
    "Describe_Weather",
]


def parse_planet(child: et.Element, text_dict: dict[str, str]):
    game_object = parse_generic_game_object(child, text_dict)
    if not game_object:
        return None

    tooltips: list[str] = []
    for tag in DESCRIPTION_TAGS:
        descriptor = child.find(tag)
        if descriptor is None:
            continue

        split_tag = tag.split("_")
        text_entry = text_entry_from_tag(descriptor, text_dict)
        if text_entry:
            tooltips.append(f"{split_tag[-1]}: {text_entry}")

    return Planet(**game_object.dict(), tooltips=tooltips)

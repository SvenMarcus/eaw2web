from typing import cast
from xml.etree import ElementTree as et

from eaw2web.gameobjecttypes import Planet
from eaw2web.text import Encyclopedia, from_csv_line
from eaw2web.xml.generic import parse_generic_game_object
from eaw2web.xml.text import text_or_empty

DESCRIPTION_TAGS = [
    "Describe_History",
    "Describe_Population",
    "Describe_Wildlife",
    "Describe_Terrain",
    "Describe_Weather",
]


def parse_planet(child: et.Element, encyclopedia: Encyclopedia):
    game_object = parse_generic_game_object(child, encyclopedia)
    if not game_object:
        return None

    tooltips: list[str] = []
    for tag in DESCRIPTION_TAGS:
        descriptor = child.find(tag)
        if descriptor is None:
            continue

        split_tag = tag.split("_")
        text_entry = encyclopedia.get_text(text_or_empty(descriptor))
        if text_entry:
            tooltips.append(f"{split_tag[-1]}: {text_entry}")

    coordinates_str = text_or_empty(child.find("Galactic_Position")) or "0,0,0"
    coordinates = tuple([float(x) for x in from_csv_line(coordinates_str)])
    coordinates = cast(tuple[float, float, float], coordinates)

    return Planet(**game_object.dict(), tooltips=tooltips, coordinates=coordinates)

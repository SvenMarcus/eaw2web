from pathlib import Path
from typing import cast
from xml.etree import ElementTree as et

from eaw2web.gameobjecttypes import (
    BuildingSlots,
    Planet,
    PlanetAbilityInformation,
    TextEntry,
)
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


def parse_planet(
    file: Path, child: et.Element, encyclopedia: Encyclopedia
) -> Planet | None:
    game_object = parse_generic_game_object(file, child, encyclopedia)
    if not game_object:
        return None

    return Planet(
        **game_object.dict(),
        coordinates=parse_coordinates(child),
        tooltips=parse_tooltips(child, encyclopedia),
        ability_info=parse_ability_information(child, encyclopedia),
        max_starbase=int(text_or_empty(child.find("Max_Space_Base")) or 0),
        building_slots=BuildingSlots(land=0, space=0),
    )


def parse_tooltips(child: et.Element, encyclopedia: Encyclopedia) -> list[TextEntry]:
    tooltips: list[TextEntry] = []

    for tag in DESCRIPTION_TAGS:
        descriptor = child.find(tag)
        if descriptor is None:
            continue

        text_entry = encyclopedia.get_text(text_or_empty(descriptor))
        if text_entry:
            tooltips.append(text_entry)

    return tooltips


def parse_coordinates(child: et.Element) -> tuple[float, float, float]:
    coordinates_str = text_or_empty(child.find("Galactic_Position")) or "0,0,0"
    coordinates = tuple([float(x) for x in from_csv_line(coordinates_str)])
    return cast(tuple[float, float, float], coordinates)


def parse_ability_information(
    child: et.Element, encyclopedia: Encyclopedia
) -> PlanetAbilityInformation:
    return PlanetAbilityInformation(
        textentry=encyclopedia.get_text(
            text_or_empty(child.find("Planet_Ability_Name"))
        ),
        icon=text_or_empty(child.find("Planet_Ability_Icon")),
    )

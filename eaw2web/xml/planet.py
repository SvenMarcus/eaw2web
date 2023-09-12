from pathlib import Path
from typing import Any, cast
from xml.etree import ElementTree as et

from eaw2web.gameobjecttypes import BuildingSlots, Planet, PlanetAbilityInformation
from eaw2web.gameobjecttypes.planet import (
    PlanetTacticalDescriptions,
    WeatherInformation,
)
from eaw2web.text import Encyclopedia, from_csv_line
from eaw2web.xml.generic import parse_generic_game_object
from eaw2web.xml.text import text_entry_from_tag, text_or_empty, collect_tooltips

DESCRIPTION_TAGS = [
    "Describe_History",
    "Describe_Population",
    "Describe_Wildlife",
    "Describe_Terrain",
    "Describe_Weather",
]


def safeint(text: Any) -> int:
    return int(float(text))


def parse_planet(
    file: Path, child: et.Element, encyclopedia: Encyclopedia
) -> Planet | None:
    game_object = parse_generic_game_object(file, child, encyclopedia)
    if not game_object:
        return None

    return Planet(
        **game_object.dict(),
        coordinates=parse_coordinates(child),
        credit_income=safeint(text_or_empty(child.find("Planet_Credit_Value")) or 0),
        ability_info=parse_ability_information(child, encyclopedia),
        weather_info=parse_weather(child, encyclopedia),
        tactical_descriptions=parse_tactical_descriptions(child, encyclopedia),
        tooltips=collect_tooltips(child, encyclopedia),
        max_starbase=safeint(text_or_empty(child.find("Max_Space_Base")) or 0),
        building_slots=parse_building_slots(child),
    )


def parse_weather(child: et.Element, encyclopedia: Encyclopedia) -> WeatherInformation:
    return WeatherInformation(
        name=text_entry_from_tag(child.find("Encyclopedia_Weather_Name"), encyclopedia),
        description=text_entry_from_tag(
            child.find("Encyclopedia_Weather_Info"), encyclopedia
        ),
        icon=text_or_empty(child.find("Encyclopedia_Weather_Icon")),
    )


def parse_tactical_descriptions(
    child: et.Element, encyclopedia: Encyclopedia
) -> PlanetTacticalDescriptions:
    descriptors = {
        tag.removeprefix("Describe_"): text_entry_from_tag(
            child.find(tag), encyclopedia
        )
        for tag in DESCRIPTION_TAGS
    }
    return PlanetTacticalDescriptions(**descriptors)


def parse_coordinates(child: et.Element) -> tuple[float, float, float]:
    coordinates_str = text_or_empty(child.find("Galactic_Position")) or "0,0,0"
    coordinates = tuple([float(x) for x in from_csv_line(coordinates_str)])[:3]
    return cast(tuple[float, float, float], coordinates)


def parse_ability_information(
    child: et.Element, encyclopedia: Encyclopedia
) -> PlanetAbilityInformation:
    return PlanetAbilityInformation(
        textentry=text_entry_from_tag(child.find("Planet_Ability_Name"), encyclopedia),
        icon=text_or_empty(child.find("Planet_Ability_Icon")),
    )


def parse_building_slots(child: et.Element) -> BuildingSlots:
    return BuildingSlots(
        land=safeint(child.findtext("Special_Structures_Land") or 0),
        space=safeint(child.findtext("Special_Structures_Space") or 0),
    )

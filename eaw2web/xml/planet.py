from pathlib import Path
from typing import cast
from xml.etree import ElementTree as et

from eaw2web.gameobjecttypes import BuildingSlots, Planet, PlanetAbilityInformation
from eaw2web.gameobjecttypes.atomics import BaseObject
from eaw2web.gameobjecttypes.planet import (
    PlanetTacticalDescriptions,
    WeatherInformation,
)
from eaw2web.text import Encyclopedia
from eaw2web.xml.generic import parse_generic_game_object
from eaw2web.xml.tags import TagParser, allow_missing
from eaw2web.xml.textentries import collect_tooltips


DESCRIPTION_TAGS = [
    "Describe_History",
    "Describe_Population",
    "Describe_Wildlife",
    "Describe_Terrain",
    "Describe_Weather",
]


def parse_planet(
    file: Path,
    child: et.Element,
    encyclopedia: Encyclopedia,
    variant: BaseObject | None = None,
) -> Planet | None:
    parser = TagParser(child)
    game_object = parse_generic_game_object(file, child, encyclopedia, variant)
    if not game_object:
        return None
    return Planet(
        **game_object.model_dump(),
        coordinates=parse_coordinates(parser),
        credit_income=allow_missing(parser.integer, "Planet_Credit_Value", fallback=0),
        ability_info=parse_ability_information(parser, encyclopedia),
        weather_info=parse_weather(parser, encyclopedia),
        tactical_descriptions=parse_tactical_descriptions(parser, encyclopedia),
        tooltips=collect_tooltips(parser, encyclopedia),
        max_starbase=parser.integer("Max_Space_Base"),
        building_slots=parse_building_slots(parser),
    )


def parse_weather(parser: TagParser, encyclopedia: Encyclopedia) -> WeatherInformation:
    return WeatherInformation(
        name=encyclopedia.get_text(
            allow_missing(parser.text, "Encyclopedia_Weather_Name", fallback="")
        ),
        description=encyclopedia.get_text(
            allow_missing(parser.text, "Encyclopedia_Weather_Info", fallback="")
        ),
        icon=allow_missing(parser.text, "Encyclopedia_Weather_Icon", fallback=""),
    )


def parse_tactical_descriptions(
    parser: TagParser, encyclopedia: Encyclopedia
) -> PlanetTacticalDescriptions:
    descriptors = {
        tag.removeprefix("Describe_"): encyclopedia.get_text(
            allow_missing(parser.text, tag, fallback="")
        )
        for tag in DESCRIPTION_TAGS
    }
    return PlanetTacticalDescriptions(**descriptors)


def parse_coordinates(parser: TagParser) -> tuple[float, float, float]:
    coordinates = parser.csv("Galactic_Position", [float, float, float])
    return cast(tuple[float, float, float], coordinates)


def parse_ability_information(
    parser: TagParser, encyclopedia: Encyclopedia
) -> PlanetAbilityInformation:
    return PlanetAbilityInformation(
        textentry=encyclopedia.get_text(
            allow_missing(parser.text, "Planet_Ability_Name", fallback="")
        ),
        icon=allow_missing(parser.text, "Planet_Ability_Icon", fallback=""),
    )


def parse_building_slots(parser: TagParser) -> BuildingSlots:
    return BuildingSlots(
        land=parser.integer("Special_Structures_Land"),
        space=parser.integer("Special_Structures_Space"),
    )

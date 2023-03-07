from typing import Any, Optional, Protocol, cast
from xml.etree.ElementTree import Element, ElementTree

from eaw2web.gameobjecttypes import BaseObject
from eaw2web.modstack import ModStack
from eaw2web.text import Encyclopedia

from eaw2web.xml.campaign import parse_campaign
from eaw2web.xml.faction import parse_faction
from eaw2web.xml.planet import parse_planet
from eaw2web.xml.traderoutes import parse_traderoute
from eaw2web.xml.units import parse_unit_object


class DataCollector(Protocol):
    def collect_all(
        self, files: list[str], encyclopedia: Encyclopedia
    ) -> list[BaseObject]:
        ...

    def collect_from(
        self, filename: str, encyclopedia: Encyclopedia
    ) -> list[BaseObject]:
        ...


class GameObjectParser(Protocol):
    def __call__(
        self, child: Element, encyclopedia: Encyclopedia
    ) -> Optional[BaseObject]:
        pass


def defaultparsers() -> dict[str, GameObjectParser]:
    return {
        "Campaign": parse_campaign,
        "Planet": parse_planet,
        "TradeRoute": parse_traderoute,
        "Faction": parse_faction,
        "SpaceUnit": parse_unit_object,
        "GroundCompany": parse_unit_object,
        "UniqueUnit": parse_unit_object,
        "HeroUnit": parse_unit_object,
    }


class GameObjectCollector:
    def __init__(
        self, mod_stack: ModStack, parsers: dict[str, GameObjectParser] | None = None
    ) -> None:
        self.mod_stack = mod_stack
        self.parsers = parsers or defaultparsers()

    def collect_from(
        self, filename: str, encyclopedia: Encyclopedia
    ) -> list[BaseObject]:
        full_path = self.mod_stack.find_topmost_xml(filename)
        tree = ElementTree(file=full_path)

        def not_none(obj: Any) -> bool:
            return obj is not None

        gameobjects = [
            self.parsers[child.tag](child, encyclopedia)
            for child in tree.getroot()
            if child.tag in self.parsers
        ]

        return cast(
            list[BaseObject],
            list(filter(not_none, gameobjects)),
        )

    def collect_all(
        self, files: list[str], encyclopedia: Encyclopedia
    ) -> list[BaseObject]:
        return [
            obj
            for file in files
            for obj in self.collect_from(file.replace("\\", "/"), encyclopedia)
        ]

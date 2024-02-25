from pathlib import Path
from typing import Protocol
from xml.etree.ElementTree import Element, ElementTree

from eaw2web.gameobjecttypes import BaseObject
from eaw2web.gameobjecttypes.variants import VariantsResolver
from eaw2web.modstack import ModStack
from eaw2web.text import Encyclopedia
from eaw2web.xml.campaign import parse_campaign
from eaw2web.xml.faction import parse_faction
from eaw2web.xml.planet import parse_planet
from eaw2web.xml.traderoutes import parse_traderoute
from eaw2web.xml.units import parse_unit_object


class DataCollector(Protocol):
    def collect_all(self, files: list[str]) -> list[BaseObject]: ...


class GameObjectParser(Protocol):
    def __call__(
        self,
        file: Path,
        child: Element,
        encyclopedia: Encyclopedia,
        variant: BaseObject | None = None,
    ) -> BaseObject | None:
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
        self,
        mod_stack: ModStack,
        encyclopedia: Encyclopedia,
        parsers: dict[str, GameObjectParser] | None = None,
    ) -> None:
        self.mod_stack = mod_stack
        self.parsers = parsers or defaultparsers()
        self.resolver = VariantsResolver(self.parsers, encyclopedia)

    def _collect_from(self, filename: str) -> None:
        stack_file = self.mod_stack.find_topmost_xml(filename)
        tree = ElementTree(file=stack_file.full_path())

        for child in tree.getroot():
            if child.tag not in self.parsers:
                continue

            self.resolver.parse(stack_file.from_root(), child)

    def collect_all(self, files: list[str]) -> list[BaseObject]:
        for file in files:
            self._collect_from(file.replace("\\", "/"))

        return self.resolver.resolve_all()

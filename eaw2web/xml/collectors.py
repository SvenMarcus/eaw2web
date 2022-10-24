from typing import Any, Generic, Optional, Protocol, TypeVar, cast
from xml.etree.ElementTree import Element, ElementTree

from eaw2web.xml.faction import parse_faction
from eaw2web.gameobjecttypes import Faction, GenericGameObject
from eaw2web.modstack import ModStack


GameObjectType = TypeVar("GameObjectType")


class DataCollector(Protocol, Generic[GameObjectType]):
    def __call__(
        self, mod_stack: ModStack, filename: str, text_dict: dict[str, str]
    ) -> list[GameObjectType]:
        ...


class GameObjectParser(Protocol):
    def __call__(
        self, child: Element, text_dict: dict[str, str]
    ) -> Optional[GenericGameObject]:
        pass


class GameObjectCollector:
    def __init__(self, parsers: dict[str, GameObjectParser]) -> None:
        self.parsers = parsers

    def __call__(
        self,
        mod_stack: ModStack,
        filename: str,
        text_dict: dict[str, str],
    ) -> list[GenericGameObject]:

        full_path = mod_stack.find_topmost_xml(filename)
        tree = ElementTree(file=full_path)

        def not_none(obj: Any) -> bool:
            return obj is not None

        gameobjects = [
            self.parsers[child.tag](child, text_dict)
            for child in tree.getroot()
            if child.tag in self.parsers
        ]

        return cast(
            list[GenericGameObject],
            list(filter(not_none, gameobjects)),
        )


class FactionCollector:
    def __call__(
        self,
        mod_stack: ModStack,
        filename: str,
        text_dict: dict[str, str],
    ) -> list[Faction]:
        full_path = mod_stack.find_topmost_xml(filename)
        tree = ElementTree(file=full_path)

        return [parse_faction(child, text_dict) for child in tree.getroot()]


def collect_from_files(
    files: list[str],
    collector: DataCollector[GameObjectType],
    mod_stack: ModStack,
    text_dict: dict[str, str],
) -> list[GameObjectType]:
    return [
        obj
        for file in files
        for obj in collector(mod_stack, file.replace("\\", "/"), text_dict)
    ]

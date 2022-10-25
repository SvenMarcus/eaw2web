from typing import Any, Optional, Protocol, cast
from xml.etree.ElementTree import Element, ElementTree

from eaw2web.gameobjecttypes import BaseObject
from eaw2web.modstack import ModStack
from eaw2web.text import Encyclopedia


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


class GameObjectCollector:
    def __init__(
        self, mod_stack: ModStack, parsers: dict[str, GameObjectParser]
    ) -> None:
        self.mod_stack = mod_stack
        self.parsers = parsers

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

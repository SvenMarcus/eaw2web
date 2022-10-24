from typing import Any, Optional, Protocol, cast
from xml.etree.ElementTree import Element, ElementTree

from eaw2web.gameobjecttypes import GenericGameObject
from eaw2web.modstack import ModStack


class DataCollector(Protocol):
    def collect_all(
        self, files: list[str], text_dict: dict[str, str]
    ) -> list[GenericGameObject]:
        ...

    def collect_from(
        self, filename: str, text_dict: dict[str, str]
    ) -> list[GenericGameObject]:
        ...


class GameObjectParser(Protocol):
    def __call__(
        self, child: Element, text_dict: dict[str, str]
    ) -> Optional[GenericGameObject]:
        pass


class GameObjectCollector:
    def __init__(
        self, mod_stack: ModStack, parsers: dict[str, GameObjectParser]
    ) -> None:
        self.mod_stack = mod_stack
        self.parsers = parsers

    def collect_from(
        self,
        filename: str,
        text_dict: dict[str, str],
    ) -> list[GenericGameObject]:

        full_path = self.mod_stack.find_topmost_xml(filename)
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

    def collect_all(
        self,
        files: list[str],
        text_dict: dict[str, str],
    ) -> list[GenericGameObject]:
        return [
            obj
            for file in files
            for obj in self.collect_from(file.replace("\\", "/"), text_dict)
        ]

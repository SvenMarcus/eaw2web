import logging

from pathlib import Path
from typing import TYPE_CHECKING
from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes.atomics import BaseObject
from eaw2web.text import Encyclopedia
from eaw2web.xml.tags import ChildNotFoundError, ParsingError
from eaw2web.xml.text import text_or_empty

if TYPE_CHECKING:
    from eaw2web.xml.collectors import GameObjectParser


class VariantsResolver:
    def __init__(
        self, parsers: dict[str, "GameObjectParser"], encyclopedia: Encyclopedia
    ) -> None:
        self._resolved: dict[str, BaseObject] = dict()
        self._unresolved: dict[str, set[tuple[Path, Element]]] = dict()
        self._parsers = parsers
        self._encyclopedia = encyclopedia

    def parse(self, file: Path, element: Element) -> None:
        variant_tag = element.find("Variant_Of_Existing_Type")
        base_object_name = text_or_empty(variant_tag)

        if base_object_name:
            unresolved_for_type = self._unresolved.setdefault(base_object_name, set())
            unresolved_for_type.add((file, element))
            return

        self._tryparse(file, element)

    def _tryparse(
        self, file: Path, element: Element, base_object: BaseObject | None = None
    ) -> BaseObject | None:
        try:
            return self._parse_element(file, element, base_object)
        except (ChildNotFoundError, ParsingError) as ex:
            logging.error(ex)
            return None

    def _parse_element(
        self, file: Path, element: Element, base_object: BaseObject | None
    ) -> BaseObject | None:
        obj = self._parsers[element.tag](
            file,
            element,
            self._encyclopedia,
            base_object,
        )

        if obj is not None:
            self._resolved[obj.xml_id] = obj

        return obj

    def resolve_all(self) -> list[BaseObject]:
        for base_object_name, unresolved_elements in self._unresolved.items():
            base_object = self._resolved.get(base_object_name)

            if not base_object:
                logging.error(f"Did not find base object {base_object_name}")
                continue

            for file, element in unresolved_elements:
                self._tryparse(file, element, base_object)

        self._unresolved = dict()
        return list(self._resolved.values())

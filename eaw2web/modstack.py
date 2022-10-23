from functools import cached_property
from pathlib import Path
from typing import Generator
from xml.etree.ElementTree import ElementTree


GameObjectFiles = "GameObjectFiles.xml"
FactionFiles = "FactionFiles.xml"


class ModStack:
    def __init__(self, mod_stack: list[str]) -> None:
        self._mod_stack = mod_stack

    def itermods(self) -> Generator[str, None, None]:
        for mod in reversed(self._mod_stack):
            yield mod

    def find_topmost_xml(self, xml_name: str) -> str:
        for stack_item in reversed(self._mod_stack):
            full_path = Path(stack_item) / "Data" / "XML" / xml_name
            if full_path.exists():
                return str(full_path)

        raise FileNotFoundError(f"Could not find {xml_name}")

    @cached_property
    def factionfiles(self) -> list[str]:
        return _get_filelist_from(self, FactionFiles)

    @cached_property
    def gameobjectfiles(self) -> list[str]:
        return _get_filelist_from(self, GameObjectFiles)


def _get_filelist_from(mod_stack: ModStack, file: str) -> list[str]:
    filepath = mod_stack.find_topmost_xml(file)
    tree = ElementTree(file=filepath)
    root = tree.getroot()
    return [file.text for file in root.findall("File") if file.text]
from pathlib import Path
from xml.etree.ElementTree import Element
from eaw2web.gameobjecttypes import BaseObject


def parse_base_object(file: Path, child: Element) -> BaseObject:
    return BaseObject(
        file=file, xml_id=child.attrib["Name"], game_object_type=child.tag
    )

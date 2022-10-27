from re import M
from xml.etree.ElementTree import Element
from eaw2web.gameobjecttypes import BaseObject


def parse_base_object(child: Element) -> BaseObject:
    return BaseObject(xml_id=child.attrib["Name"], game_object_type=child.tag)

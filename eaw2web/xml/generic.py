from xml.etree.ElementTree import Element
from eaw2web.gameobjecttypes import GenericGameObject
from eaw2web.text import Encyclopedia
from eaw2web.xml.base import parse_base_object
from eaw2web.xml.text import text_or_empty


def parse_generic_game_object(child: Element, encyclopedia: Encyclopedia):
    return GenericGameObject(
        **parse_base_object(child).dict(),
        text=encyclopedia.get_text(text_or_empty(child.find("Text_ID"))),
        variant_of=text_or_empty(child.find("Variant_Of_Existing_Type")),
    )

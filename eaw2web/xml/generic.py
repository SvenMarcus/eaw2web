from xml.etree.ElementTree import Element
from eaw2web.gameobjecttypes import GenericGameObject
from eaw2web.text import text_entry_from_tag


def parse_generic_game_object(child: Element, text_dict: dict[str, str]):
    text_id_tag = find_or_empty(child, "Text_ID")
    variant = find_or_empty(child, "Variant_Of_Existing_Type")

    return GenericGameObject(
        game_object_type=child.tag,
        xml_id=child.attrib["Name"],
        text=text_entry_from_tag(text_id_tag, text_dict),
        variant_of=variant.text or "",
    )


def find_or_empty(element: Element, tag: str) -> Element:
    child = element.find(tag)
    return child if child is not None else Element("")

from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import Unit
from eaw2web.text import Encyclopedia
from eaw2web.xml.generic import parse_generic_game_object
from eaw2web.xml.icon import icon_name
from eaw2web.xml.text import collect_tooltips, text_or_empty


def parse_unit_object(child: Element, encyclopedia: Encyclopedia):
    return Unit(
        **parse_generic_game_object(child, encyclopedia).dict(),
        icon=icon_name(child),
        tooltips=collect_tooltips(child, encyclopedia),
        affiliation=affiliation(child),
        tech_level=text_or_empty(child.find("Tech_Level")),
    )


def affiliation(child: Element):
    affiliation_text = text_or_empty(child.find("Affiliation"))
    split_affiliation = affiliation_text.split(",")
    return [
        affiliation.strip() for affiliation in split_affiliation if affiliation.strip()
    ]

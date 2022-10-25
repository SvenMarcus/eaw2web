from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import Faction
from eaw2web.text import Encyclopedia
from eaw2web.xml.generic import parse_generic_game_object
from eaw2web.xml.icon import icon_name


def parse_faction(child: Element, encyclopedia: Encyclopedia):
    return Faction(
        **(parse_generic_game_object(child, encyclopedia).dict()),
        icon=icon_name(child),
    )

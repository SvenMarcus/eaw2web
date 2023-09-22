from pathlib import Path
from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import TradeRoute
from eaw2web.gameobjecttypes.atomics import BaseObject
from eaw2web.text import Encyclopedia
from eaw2web.xml.text import text_or_empty


def parse_traderoute(
    file: Path,
    child: Element,
    encyclopedia: Encyclopedia,
    variant: BaseObject | None = None,
) -> TradeRoute:
    return TradeRoute(
        file=file,
        xml_id=child.attrib["Name"],
        game_object_type=child.tag,
        point_a=text_or_empty(child.find("Point_A")),
        point_b=text_or_empty(child.find("Point_B")),
    )

from pathlib import Path
from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import Faction
from eaw2web.gameobjecttypes.atomics import BaseObject
from eaw2web.text import Encyclopedia, bool_from_str
from eaw2web.xml.generic import parse_generic_game_object
from eaw2web.xml.icon import icon_name
from eaw2web.xml.text import text_or_empty


def parse_faction(
    file: Path,
    child: Element,
    encyclopedia: Encyclopedia,
    variant: BaseObject | None = None,
) -> Faction:
    return Faction(
        **(parse_generic_game_object(file, child, encyclopedia, variant).model_dump()),
        icon=icon_name(child),
        is_playable=bool_from_str(text_or_empty(child.find("Is_Playable"))),
    )

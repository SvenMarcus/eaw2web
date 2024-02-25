from pathlib import Path
from typing import cast
from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import Unit
from eaw2web.gameobjecttypes.atomics import BaseObject
from eaw2web.text import Encyclopedia
from eaw2web.xml.generic import parse_generic_game_object
from eaw2web.xml.icon import icon_name
from eaw2web.xml.tags import TagParser, allow_missing
from eaw2web.xml.textentries import collect_tooltips


def parse_unit_object(
    file: Path,
    child: Element,
    encyclopedia: Encyclopedia,
    variant: BaseObject | None = None,
) -> Unit:
    parser = TagParser(child)
    return Unit(
        **parse_generic_game_object(file, child, encyclopedia, variant).model_dump(),
        icon=icon_name(child),
        tooltips=collect_tooltips(parser, encyclopedia),
        affiliation=list(
            allow_missing(
                parser.csv, "Affiliation", fallback=cast(tuple[str, ...], tuple())
            ),
        ),
        tech_level=allow_missing(parser.integer, "Tech_Level", fallback=0),
    )

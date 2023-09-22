from pathlib import Path
from xml.etree.ElementTree import Element
from eaw2web.gameobjecttypes import GenericGameObject
from eaw2web.gameobjecttypes.atomics import BaseObject
from eaw2web.text import Encyclopedia
from eaw2web.xml.base import parse_base_object
from eaw2web.xml.tags import TagParser, allow_missing


def parse_generic_game_object(
    file: Path, child: Element, encyclopedia: Encyclopedia, variant: BaseObject | None
) -> GenericGameObject:
    parser = TagParser(child)
    return GenericGameObject(
        **parse_base_object(file, child).dict(),
        textentry=encyclopedia.get_text(
            allow_missing(
                parser.text,
                "Text_ID",
                fallback="",
            )
        ),
        variant_of=variant,
    )

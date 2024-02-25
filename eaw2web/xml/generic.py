from pathlib import Path
from xml.etree.ElementTree import Element
from eaw2web.gameobjecttypes import GenericGameObject
from eaw2web.gameobjecttypes.atomics import TGameObject
from eaw2web.text import Encyclopedia
from eaw2web.xml.base import parse_base_object
from eaw2web.xml.tags import TagParser, allow_missing


def parse_generic_game_object(
    file: Path, child: Element, encyclopedia: Encyclopedia, variant: TGameObject | None
) -> GenericGameObject[TGameObject]:
    parser = TagParser(child)
    return GenericGameObject(
        **parse_base_object(file, child).model_dump(),
        textentry=encyclopedia.get_text(
            allow_missing(
                parser.text,
                "Text_ID",
                fallback="",
            )
        ),
        variant_of=variant,
    )

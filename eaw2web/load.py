from functools import lru_cache
from eaw2web.config import Config
from eaw2web.gameobjecttypes import GenericGameObject
from eaw2web.modstack import ModStack
from eaw2web.text import parse_to_text_dict
from eaw2web.xml.collectors import DataCollector, GameObjectType, collect_from_files


def should_include(object: GenericGameObject, excluded_name_fragments: set[str]):
    return all(fragment not in object.xml_id for fragment in excluded_name_fragments)


@lru_cache
def parse_all_text_files(files: list[str]) -> dict[str, str]:
    text_dict: dict[str, str] = {}
    for csv in files:
        text_dict.update(parse_to_text_dict(csv))

    return text_dict


def load(
    config: Config,
    mod_stack: ModStack,
    collector: DataCollector[GameObjectType],
    files: list[str],
) -> list[GameObjectType]:
    text_dict = parse_all_text_files(config.includes.textcsv)  # type: ignore
    return collect_from_files(files, collector, mod_stack, text_dict)

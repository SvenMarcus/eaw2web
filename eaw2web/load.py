from eaw2web.config import Config
from eaw2web.gameobjecttypes import GenericGameObject
from eaw2web.text import parse_to_text_dict
from eaw2web.xml.collectors import DataCollector


def should_include(object: GenericGameObject, excluded_name_fragments: set[str]):
    return all(fragment not in object.xml_id for fragment in excluded_name_fragments)


def parse_all_text_files(files: list[str]) -> dict[str, str]:
    text_dict: dict[str, str] = {}
    for csv in files:
        text_dict.update(parse_to_text_dict(csv))

    return text_dict


def load(
    config: Config,
    collector: DataCollector,
    files: list[str],
) -> list[GenericGameObject]:
    text_dict = parse_all_text_files(config.includes.textcsv)
    return collector.collect_all(files, text_dict)

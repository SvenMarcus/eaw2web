from eaw2web.config import Config
from eaw2web.gameobjecttypes import BaseObject
from eaw2web.text import Encyclopedia
from eaw2web.xml.collectors import DataCollector


def should_include(object: BaseObject, excluded_name_fragments: set[str]):
    return all(fragment not in object.xml_id for fragment in excluded_name_fragments)


def load(
    config: Config,
    collector: DataCollector,
    files: list[str],
) -> list[BaseObject]:
    text_dict = Encyclopedia(config.includes.textcsv)
    return [
        object
        for object in collector.collect_all(files, text_dict)
        if should_include(object, config.excludes.fragments)
    ]

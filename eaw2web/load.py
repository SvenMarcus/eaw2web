from eaw2web.config import Config
from eaw2web.gameobjecttypes import BaseObject
from eaw2web.xml.collectors import DataCollector


def skip(object: BaseObject, excluded_name_fragments: set[str]) -> bool:
    return any(fragment in object.xml_id for fragment in excluded_name_fragments)


def load(
    config: Config,
    collector: DataCollector,
    files: list[str],
) -> list[BaseObject]:
    return [
        obj
        for obj in collector.collect_all(files)
        if not skip(obj, config.excludes.fragments)
    ]

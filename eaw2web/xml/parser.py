from eaw2web.modstack import ModStack
from eaw2web.xml.collectors import (
    DataCollector,
    GameObjectType,
)


def collect_from_files(
    files: list[str],
    collector: DataCollector[GameObjectType],
    mod_stack: ModStack,
    text_dict: dict[str, str],
) -> list[GameObjectType]:
    return [
        obj
        for file in files
        for obj in collector(mod_stack, file.replace("\\", "/"), text_dict)
    ]

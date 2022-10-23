from typing import Protocol
from eaw2web.modstack import ModStack
from eaw2web.xml.collectors import DataCollector, GameObjectType


class ReportProgess(Protocol):
    def begin(self, filename: str) -> None:
        ...

    def finish(self) -> None:
        ...


def reporting_collector(
    collector: DataCollector[GameObjectType],
    progress: ReportProgess,
) -> DataCollector[GameObjectType]:
    def _collector(
        mod_stack: ModStack,
        filename: str,
        text_dict: dict[str, str],
    ) -> list[GameObjectType]:
        progress.begin(filename)
        result = collector(mod_stack, filename, text_dict)
        progress.finish()
        return result

    return _collector

from typing import Protocol
from eaw2web.modstack import ModStack
import eaw2web.xml.parser as parser


class ReportProgess(Protocol):
    def begin(self, filename: str) -> None:
        ...

    def finish(self) -> None:
        ...


def into_reporting_collector(
    collector: parser.DataCollector[parser.GameObjectType],
    progress: ReportProgess,
) -> parser.DataCollector[parser.GameObjectType]:
    def _collector(
        mod_stack: ModStack,
        filename: str,
        text_dict: dict[str, str],
    ) -> list[parser.GameObjectType]:
        progress.begin(filename)
        result = collector(mod_stack, filename, text_dict)
        progress.finish()
        return result

    return _collector

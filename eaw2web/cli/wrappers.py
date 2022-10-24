from typing import Protocol
from eaw2web.gameobjecttypes import GenericGameObject
from eaw2web.xml.collectors import DataCollector


class ReportProgess(Protocol):
    def begin(self, filename: str) -> None:
        ...

    def finish(self) -> None:
        ...


def reporting_collector(collector: DataCollector, report: ReportProgess):
    original = collector.collect_from

    def collect_from(
        filename: str, text_dict: dict[str, str]
    ) -> list[GenericGameObject]:
        report.begin(filename)
        result = original(filename, text_dict)
        report.finish()
        return result

    collector.collect_from = collect_from
    return collector

from typing import Optional, Protocol
from eaw2web.gameobjecttypes import BaseObject
from eaw2web.text import Encyclopedia
from eaw2web.xml.collectors import DataCollector


class ReportProgess(Protocol):
    def begin(self, filename: str) -> None:
        ...

    def finish(self, error: Optional[Exception] = None) -> None:
        ...


def reporting_collector(collector: DataCollector, report: ReportProgess):
    original = collector.collect_from

    def collect_from(filename: str, encyclopedia: Encyclopedia) -> list[BaseObject]:
        report.begin(filename)
        error = None
        try:
            result = original(filename, encyclopedia)
        except Exception as err:
            error = err
            result = []

        report.finish(error)
        return result

    setattr(collector, "collect_from", collect_from)
    return collector

from typing import Optional, Protocol
from eaw2web.xml.collectors import DataCollector


class ReportProgess(Protocol):
    def begin(self, filename: str) -> None:
        ...

    def finish(self, error: Optional[Exception] = None) -> None:
        ...


def reporting_collector(
    collector: DataCollector, report: ReportProgess
) -> DataCollector:
    original = collector._collect_from  # type: ignore

    def collect_from(filename: str) -> None:
        report.begin(filename)
        error = None
        try:
            original(filename)
        except Exception as err:
            error = err

        report.finish(error)

    setattr(collector, "collect_from", collect_from)
    return collector

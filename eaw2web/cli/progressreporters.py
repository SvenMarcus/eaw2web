from typing import Optional
from rich.progress import Progress, TaskID
from rich.spinner import Spinner


class RichProgressReporter:
    def __init__(self, progress_bar: Progress, task_id: TaskID = TaskID(0)) -> None:
        self.bar = progress_bar
        self.task_id = task_id

    def begin(self, filename: str) -> None:
        self.bar.log(self.spinner(filename))

    def spinner(self, filename: str) -> Spinner:
        return Spinner(
            "dots",
            f"Processing {filename}",
            style="blue",
        )

    def finish(self, error: Optional[Exception] = None) -> None:
        if error:
            self.bar.log(f"[red]{error}[/red]")
        self.bar.advance(self.task_id, 1)
